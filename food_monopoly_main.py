import random
import openai
import json
import os

class FoodMonopolyGame:
    def __init__(self):
        self.map = self.generate_map()
        self.player_position = 0
        self.eaten_foods = []
        self.openai_api_key = input("Enter your OpenAI API key: ")
        openai.api_key = self.openai_api_key
        self.capitals = {
            "USA": "Washington, D.C.",
            "France": "Paris",
            "Italy": "Rome",
            "Japan": "Tokyo",
            "China": "Beijing",
            "Mexico": "Mexico City",
            "India": "New Delhi",
            "Thailand": "Bangkok",
            "Greece": "Athens",
            "Spain": "Madrid",
            "Turkey": "Ankara",
            "Korea": "Seoul",
            "Germany": "Berlin",
            "Brazil": "Brasilia",
            "Australia": "Canberra",
            "Canada": "Ottawa",
            "Taiwan": "Taipei",
            "Argentina": "Buenos Aires",
            "Vietnam": "Hanoi",
            "Russia": "Moscow"
        }

    def generate_map(self):
        countries = [
            "USA", "France", "Italy", "Japan", "China", "Mexico",
            "India", "Thailand", "Greece", "Spain", "Turkey",
            "Korea", "Germany", "Brazil", "Australia", "Canada",
            "Taiwan", "Argentina", "Vietnam", "Russia"
        ]
        random.shuffle(countries)
        return countries

    def display_instructions(self):
        print("=" * 40)
        print("""
$$$$$$$$\                           $$\       $$\      $$\                                                   $$\           $$
$$  _____|                          $$ |      $$$\    $$$ |                                                  $$ |          $$ |
$$ |       $$$$$$\   $$$$$$\   $$$$$$$ |      $$$$\  $$$$ | $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  $$ |$$\   $$\ $$ |
$$$$$\    $$  __$$\ $$  __$$\ $$  __$$ |      $$\$$\$$ $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$ |$$ |  $$ |$$ |
$$  __|   $$ /  $$ |$$ /  $$ |$$ /  $$ |      $$ \$$$  $$ |$$ /  $$ |$$ |  $$ |$$ /  $$ |$$ /  $$ |$$ /  $$ |$$ |$$ |  $$ |\__|
$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |      $$ |\$  /$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |
$$ |      \$$$$$$  |\$$$$$$  |\$$$$$$$ |      $$ | \_/ $$ |\$$$$$$  |$$ |  $$ |\$$$$$$  |$$$$$$$  |\$$$$$$  |$$ |\$$$$$$$ |$$
\__|       \______/  \______/  \_______|      \__|     \__| \______/ \__|  \__| \______/ $$  ____/  \______/ \__| \____$$ |\__|
                                                                                         $$ |                    $$\   $$ |
                                                                                         $$ |                    \$$$$$$  |
                                                                                         \__|                     \______/     """)
        print("玩法介紹：")
        print("1. 玩家從起點開始，每回合擲骰子前進 1-6 步。")
        print("2. 每當到達一個國家，您將獲得該國的美食介紹。")
        print("3. 您可以選擇挑戰，回答該國的首都名稱以吃到美食。")
        print("4. 若回答正確，可獲得該美食；若回答錯誤，將無法獲得。")
        print("5. 當玩家累積吃到 5 個美食時，遊戲獲勝！")
        print("6. 隨時可以退出遊戲或查看已吃美食。\n")
        print("祝您旅途愉快，開始探索世界美食吧！")
        print("=" * 40 + "\n")

    def roll_dice(self):
        return random.randint(1, 6)

    def generate_food_intro(self, country):
        prompt = f"請用100字形容這個{country}的一種具體有名字的特色美食"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def ask_capital(self, country):
        correct_capital = self.capitals.get(country, "").lower()
        return correct_capital

    def save_food_to_collection(self, food_intro):
        try:
            with open("food_collection.txt", "a", encoding="utf-8") as file:
                if file.tell() == 0:
                    file.write("我的美食大富翁之美食紀錄手冊:\n")
                file.write("\n" + food_intro + "\n")
                print("美食已新增到美食紀錄手冊！\n")
        except Exception as e:
            print(f"儲存美食介紹時出錯: {e}")

    def play_turn(self):
        dice = self.roll_dice()
        print(f"\n您擲出了 {dice} 點數！")
        self.player_position = (self.player_position + dice) % len(self.map)
        country = self.map[self.player_position]
        print(f"您來到了 {country}！")

        food_intro = self.generate_food_intro(country)
        print(f"\n美食介紹：\n{food_intro}\n")

        while True:
            print("選項：")
            print("1. 挑戰美食")
            print("2. 擲下一輪骰子")
            print("3. 查看已吃美食")
            print("4. 查看地圖")
            print("5. 退出遊戲")
            choice = input("請選擇操作 (1/2/3/4/5)： ").strip()

            if choice == "1":
                capital = input(f"請輸入 {country} 的首都(請用英文與首字大寫回答)： ").strip().lower()
                correct_capital = self.ask_capital(country)
                if capital == correct_capital:
                    print(f"正確！您成功品嚐了 {country} 的美食！\n")
                    self.eaten_foods.append(country)
                    self.save_food_to_collection(food_intro)

                    if len(self.eaten_foods) >= 5:
                        print("🎉 恭喜！您已經品嚐了 5 道美食，遊戲勝利！ 🎉")
                        return True
                else:
                    print(f"很遺憾，答案錯誤！{country} 的首都是 {correct_capital}。\n")

            elif choice == "2":
                dice = self.roll_dice()
                print(f"\n您擲出了 {dice} 點數！")
                self.player_position = (self.player_position + dice) % len(self.map)
                country = self.map[self.player_position]
                print(f"您來到了 {country}！")
                food_intro = self.generate_food_intro(country)
                print(f"\n美食介紹：\n{food_intro}\n")

            elif choice == "3":
                print("\n已吃國家美食清單：", ", ".join(self.eaten_foods) if self.eaten_foods else "目前尚未品嚐美食。", "\n")

            elif choice == "4":
                self.draw_map()

            elif choice == "5":
                print("感謝遊玩，歡迎再來挑戰。")
                return False

            else:
                print("無效選項，請重新選擇。\n")
        return False


    def draw_map(self):
        print("\n遊戲地圖：\n")
        map_size = 6
        cell_width = 14
        horizontal_line = "+" + "+".join(["-" * cell_width for _ in range(map_size)]) + "+"

        for i in range(map_size):
            print(horizontal_line)
            if i == 0:
                # 第一行：完整顯示前 6 個國家
                row = "| " + " | ".join(f"{self.map[j]:<{cell_width-2}}" for j in range(6)) + " |"
            elif i == map_size - 1:
                # 最後一行：顯示最後 6 個國家（倒序）
                row = "| " + " | ".join(f"{self.map[15 - j]:<{cell_width-2}}" for j in range(6)) + " |"
            else:
                # 中間的行：顯示兩側國家，中間空白
                left_country = self.map[20 - i ]
                right_country = self.map[5 + i ]
                row = f"| {left_country:<{cell_width-1}}|" + " " * (cell_width * (map_size - 2) + (map_size - 3)) + f"| {right_country:<{cell_width-2}} |"
            print(row)
        print(horizontal_line)
        print()

    def start_game(self):
        self.display_instructions()
        input("(按ENTER查看美食地圖，起點為左上角之國家)")
        self.draw_map()
        while len(self.eaten_foods) < 5:
            if not self.play_turn():
                break


game = FoodMonopolyGame()
game.start_game()