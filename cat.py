import streamlit as st
import random

# 🐱 定义猫类
class Cat:
    def __init__(self, name, hungry_index, digest_index):
        self.name = name
        self.hungry_index = hungry_index
        self.digest_index = digest_index

    def check_status(self):
        if self.hungry_index < 0 or self.digest_index < 0:
            st.warning("注意：你的猫咪状态危险！")
        self.hungry_index = max(0, self.hungry_index)
        self.digest_index = max(0, self.digest_index)

    def eat(self, amount=10):
        st.write(f"{self.name} 正在吃饭...")
        self.hungry_index -= amount
        self.digest_index += amount // 2
        self.check_status()

    def poop(self, amount=15):
        st.write(f"{self.name} 去上厕所了...")
        self.digest_index -= amount
        self.check_status()

    def update_status(self, time_passed=1):
        self.hungry_index += 5 * time_passed
        self.digest_index -= 3 * time_passed
        self.check_status()

    def show(self):
        st.write(f"🐾 {self.name}：饥饿值 = {self.hungry_index}%；消化值 = {self.digest_index}%")


# 🖥️ Streamlit 前端界面
st.title("小猫Saturn生活模拟器")

# --- 用户输入 ---
name = st.text_input("请输入猫咪的名字：", "Saturn")
initial_hungry = st.number_input("初始饥饿值（0–100%）：", 0, 100, random.randint(50, 100))
initial_digest = st.number_input("初始消化值（0–100%）：", 0, 100, random.randint(50, 100))
loop_count = st.number_input("请设定模拟的回合数：", 1, 20, 3)

# --- 创建猫对象 ---
cat = Cat(name, initial_hungry, initial_digest)

# --- 按钮开始模拟 ---
if st.button("开始模拟 🐾"):
    st.success(f"开始模拟 {cat.name} 的日常生活！")

    for i in range(loop_count):
        st.markdown(f" 第 {i+1} 回合")
        cat.eat()
        cat.poop()
        cat.update_status()
        cat.show()
        st.divider()
