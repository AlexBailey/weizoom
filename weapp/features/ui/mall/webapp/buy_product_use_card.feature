#_author_ "师帅8.27"
Feature:在webapp使用微众卡购买商品
#后台开启后,手机端购买时显示微众卡,否则不显示
#1.使用一张微众卡，卡内金额大于购买商品金额
#2.使用一张微众卡，卡内金额等于购买商品金额
#3.使用一张微众卡，卡内金额小于购买商品金额，可以添加多张微众卡购买，最多10张
#4.使用微众卡时，输入账号，不输入密码，提示“请输入密码”，输入密码，不输入账号，提示“请输入卡号”，输入错误的账号和密码，提示“卡号或密码错误”;都为空时不输入,提示"请输入卡号"
#5.使用已用完的微众卡购买商品
#6.使用未激活的微众卡购买商品
#7.使用已过期微众卡购买商品
#8.使用两张同样的微众卡购买
#9.使用10张微众卡后，不能在添加第11张