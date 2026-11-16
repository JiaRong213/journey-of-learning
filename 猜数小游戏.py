import random

MAX_TRIES = 7

def play_game():
    anwser = random.randint(1, 100)
    for i in range(1,MAX_TRIES+1):
        guess = int(input("请输入一个1到100之间的整数: "))
        if guess < anwser:
            print("太小了！")
        elif guess > anwser:
            print("太大了！")
        else:
            print(f"恭喜你，猜对了！答案是{anwser}。你用了{i}次机会。")
            return
    print(f"很遗憾，机会用完了。答案是{anwser}。")

if __name__ == "__main__":
    play_game()