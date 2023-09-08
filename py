#! /bin/bash
# ubuntu环境下使用虚拟Python环境运行脚本:  ./Py  main.py
PYEnv_DIR="/root/PYEnv/bin"
source $PYEnv_DIR/activate
if [ $# -eq 0 ]; then
  echo "没有传递任何参数。"
else
	$PYEnv_DIR/python3 $@
fi
