import marimo

__generated_with = "0.9.9"
app = marimo.App(width="medium")


@app.cell
def __():
    from prover import Prover

    prover = Prover()
    return Prover, prover


@app.cell
def __(prover):
    claim = "Abortion is moral"
    out = None
    for x in prover.run(proposition_claim=claim, use_small_model=False):
        out = x
        print(out['status'])
    arg1_w_claims = out['arg1_w_claims']
    arg2_w_claims = out['arg2_w_claims']
    print(arg1_w_claims, arg2_w_claims)
    print(f"Winning Claim: {out['victor']}")
    return arg1_w_claims, arg2_w_claims, claim, out, x


if __name__ == "__main__":
    app.run()
