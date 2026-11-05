import argparse
from common import ask, available

def run(prompt, providers, max_tokens, temperature):
    rows = []
    for p in providers:
        print("=" * 72)
        try:
            r = ask(p, prompt, max_tokens=max_tokens, temperature=temperature)
        except Exception as e:
            print(f"[{p}] FAILED: {e}"); continue
        cost = "n/a" if r["cost"] is None else f"${r['cost']:.6f}"
        print(f"Provider : {r['provider']}  (model: {r['model']})")
        print(f"Time     : {r['seconds']} s")
        print(f"Tokens   : {r['input_tokens']} in + {r['output_tokens']} out = {r['tokens']}")
        print(f"Est. cost: {cost}  (list-price estimate; free tier mein asal kharcha $0)")
        print("-" * 72); print(r["text"]); rows.append(r)
    if rows:
        print("\n" + "=" * 72 + "\nSUMMARY")
        print(f"{'Provider':<10}{'Model':<28}{'Time(s)':>8}{'Tokens':>8}{'Est.$':>12}")
        for r in rows:
            c = "n/a" if r["cost"] is None else f"{r['cost']:.6f}"
            print(f"{r['provider']:<10}{r['model']:<28}{r['seconds']:>8}{r['tokens']:>8}{c:>12}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="LLM Showdown: ek prompt, kai providers")
    ap.add_argument("prompt", nargs="?", help="prompt (na diya to puchha jayega)")
    ap.add_argument("-p", "--providers", nargs="+", help="jaise: Groq Gemini (default: sab available)")
    ap.add_argument("--max-tokens", type=int, default=800)
    ap.add_argument("--temperature", type=float, default=0.7)
    a = ap.parse_args()
    prompt = a.prompt or input("Enter your prompt: ")
    provs = a.providers or available()
    print("Providers:", provs)
    run(prompt, provs, a.max_tokens, a.temperature)
