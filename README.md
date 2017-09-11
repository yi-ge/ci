最简持续集成服务器管理系统
==========================

Python 依赖版本：3.6.2

### 安装虚拟环境（可选）

```
$ sudo pip install virtualenv virtualenvwrapper
```

It will probably install virtualenv on your system. Maybe it’s even in your package manager.

If you use Ubuntu, try:

```
$ sudo apt-get install python-virtualenv virtualenvwrapper
```

MAC在`~/.bash_profile`（Ubuntu等Linux系统在`~/.bashrc`）文件中添加以下代码：

```
export WORKON_HOME=$HOME/WorkStation
export VIRTUALENVWRAPPER_PYTHON=`which python`
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
```

然后`source ~/.bash_profile`或者`source ~/.bashrc`。

**常用命令：**

```
workon # 列出已有环境
workon XXX # 进入XXX环境
mkvirtualenv XXX # 创建XXX环境
deactivate XXX # 退出XXX环境
rmvirtualenv XXX # 删除XXX环境
```

Ps：如果你嫌虚拟环境麻烦，也可以试试用[p](https://github.com/qw3rtman/p)或[pyenv](https://github.com/pyenv/pyenv)。需要注意的是，目前p不支持对pip的管理。

### 安装基础工具pipenv

需事先安装Python3.6.2

如果没有安装上述虚拟环境：

```
$ pip install --user pipenv
```

如果已经安装则进入项目目录执行：

```
$ mkvirtualenv -p python3 ci
$ pip install pipenv
```

### 安装依赖

```
$ pipenv install
```

### 运行应用程序

```
$ export FLASK_APP=manage.py
$ flask run --host=0.0.0.0
```
