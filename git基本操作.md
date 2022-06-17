# 第一次上传文件到GitHub
略

# 第二次以及之后上传文件到GitHub
1. 点击git bash here，进入cmd操作界面
2. 输入git add . (.代表将当前目录所有文件加入到缓存区)
    - 输入git add ‘file’，（代表只把file文件加入缓存区）
    - git rm “file” （从缓存区删除文件）
3. （可选）git status 查看现在的状态（是否提交）
4. git commit 提交文件到本地仓库
    - git commit -m “添加提交备注”
5. git push 推送到远程仓库
    - git push -u origin master 第一次提交需要这样写，表示将本地仓库推送到远程仓库，其他时候只用写git push 即可
	- 推送时可能遇到关羽SSL的fail如“OpenSSL SSL_read: Connection was reset, errno 10054”，只需输入git config --global http.sslVerify "false"
# 拉取代码
git clone https://github.com/MatchlessHeroVIP/ssmtest.git
git pull
# 撤销修改
1. 如果一个文件修改后未提交也未添加：
-   所谓提交，即执行了git commit命令
-   所谓添加，即执行了git add命令
撤销修改使用：
git checkout “file”

查看一个文件的修改可以使用：
git diff
2. 撤销一个已添加未提交的修改：
    - 先试用reset命令取消添加： git reset “file”
    - 再执行git check “file”

# 查看提交记录
git log
1. 如果提交记录很多，可以在命令中加上 -n参数，表示我们只想看到一条记录，如下所示：
    git log  -1
2. 如果想要查看查询的这条提交记录中具体修改了什么内容，可以在命令中加入 -p参数，命令如下所示：
    git log -1 -p
查询的结果中，减号代表删除的部分，加号代表增加的部分
按q键退出