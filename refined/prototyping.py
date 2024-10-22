import marimo

__generated_with = "0.9.9"
app = marimo.App(width="medium")


@app.cell
def __():
    from prover import prover



    claim = "9mm is just as effective as 0.40 caliber and 0.45 caliber bullets in gun fights"
    out = None
    for x in prover(claim):
        out = x
        print(out['status'])
        # if "opposition_claim" in out:
        #     print(out['opposition_claim'])
    arg1_w_claims = out['arg1_w_claims']
    arg2_w_claims = out['arg2_w_claims']
    print(arg1_w_claims, arg2_w_claims)
    print(f"Winning Claim: {out['victor']}")
    return arg1_w_claims, arg2_w_claims, claim, out, prover, x


if __name__ == "__main__":
    app.run()
