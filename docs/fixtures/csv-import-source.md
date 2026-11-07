# CSV 导入服务源码摘录（教学用简化服务；仅以下行为有依据）

数据库记录：
ImportJob {id, owner_id, dataset_id, status, committed_line}
Submission {owner_id, request_key, input_hash, job_id}
ImportEvent {job_id, sequence, kind, detail}

POST /imports 使用当前登录者核对 dataset 权限。
同 owner_id + request_key 的 Submission 已存在时，比较 input_hash；相同返回原 job，不同报 submission_conflict。
新任务在一次事务中写入 Submission、ImportJob(status=queued, committed_line=0)、accepted事件。

Dispatcher：每个 dataset_id 最多启动一个正在导入的 job；不同 dataset 可并行。每次只挑已到 retry_after 的 queued 任务。
读取文件由解析器处理，解析器的内存字段包含当前行及未提交的行数组。解析器不是持久数据。
每批最多100行。在同一数据库事务中：插入本批数据，更新 ImportJob.committed_line 为已提交的最后一行，追加 batch_committed 事件。
事务失败时本批全部回滚，内存行不会因此成为已导入结果。

I/O暂时错误：保存错误事件，job置queued并设置稍后retry_after；重新启动解析器，跳过committed_line及其以前的行，重读未提交部分。
用户取消：job置cancelled，不再自动调度；已经提交的数据保留，不自动撤销。
文件解析错误：job置failed并报告原文件行号；不得把错误行默默丢掉后标success。
完整文件各批均提交后，job置completed并追加completed事件。

GET /imports/:job_id 先核对用户权限，返回持久job状态和最近事件。浏览器关闭不触发取消。
代码不包含断点时的解析器内存快照，不包含跨Server调度协调，也没有科学数据有效性判断。
