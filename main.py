"""Point d'entrée : python main.py "votre question" """
import json
import sys

from src.pipeline.answer import answer

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Question de test ?"
    print(json.dumps(answer(question), ensure_ascii=False, indent=2))
