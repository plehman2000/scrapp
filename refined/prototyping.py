import marimo

__generated_with = "0.9.9"
app = marimo.App(width="medium")


@app.cell
def __():
    from prover import prover



    claim = "It's possible that 9/11 was a false flag"
    out = None
    for x in prover(claim, opposition_claim = "9/11 wasn't a false flag"):
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
