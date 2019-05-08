import random


def ask_questions(qs_and_as):

    num_qs_and_as = len(qs_and_as)

    while True:
        cur = 0
        while cur <= num_qs_and_as:
            if cur == num_qs_and_as - 1 or random.randint(0, 2) == 0:
                i = 0
                for q_and_a in qs_and_as:
                    print("%-10s= %d" % (q_and_a[0], q_and_a[1]), end="")
                    if i == cur:
                        print("  <==")
                    else:
                        print()
                    i = i + 1
                    q_and_a = qs_and_as[cur]
                del qs_and_as[cur]

                if ask_question(q_and_a):
                    qs_and_as.append(q_and_a)
                else:
                    qs_and_as.insert(0, q_and_a)

                cur = 0
            else:
                cur = cur + 1


def ask_question(q_and_a):
    q = q_and_a[0]
    a = q_and_a[1]

    try:
        user_answer = int(input(q + "? "))
    except ValueError:
        user_answer = 0
    if user_answer == a:
        input("Correct.")
        return True
    else:
        input("False. Correct answer is %d." % a)
        return False


if __name__ == "__main__":
    qs_and_as = []
    min_a = 11
    max_a = max_b = 15
    a = min_a

    while a <= max_a:
        b = a
        while b <= max_b:
            qs_and_as.append([f"{a} * {b}", a * b])
            b = b + 1
        a = a + 1

    ask_questions(qs_and_as)
