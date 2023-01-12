import json
import random

import disnake

class Hyakunin_Isshu_Manager:
    def __init__(self):
        with open('resource/hyakushu.json') as f:
            self.hyakushu = json.loads(f.read())

        with open('resource/kimariji.json') as f:
            self.kimariji = json.loads(f.read())

    def generate_random_button(self):
        simonoku_list = list(self.hyakushu.values())
        answer_simonoku = random.choice(simonoku_list)
        simonoku_list.remove(answer_simonoku)

        answer_kaminoku = [k for k, v in self.hyakushu.items() if v == answer_simonoku]

        self.answer_kaminoku = answer_kaminoku
        self.answer_simonoku = answer_simonoku
        self.simonoku_list = simonoku_list

        return answer_kaminoku[0], answer_simonoku

    def generate_button(self, view):
        row_list = [1, 2, 3, 4, 5]
        answer_row = random.choice(row_list)
        row_list.remove(answer_row)

        for row in row_list:
            view.add_item(
                disnake.ui.Button(
                    label=random.choice(self.simonoku_list),
                    style=disnake.ButtonStyle.grey,
                    custom_id=str(row),
                    row=row,
                )
            )

        view.add_item(
            disnake.ui.Button(
                label=self.answer_simonoku,
                style=disnake.ButtonStyle.grey,
                custom_id=str(answer_row),
                row=answer_row,
            )
        )

        return view

if __name__ == "__main__":
    s = Hyakunin_Isshu_Manager()
    print(s.generate_random_button())
