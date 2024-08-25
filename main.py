from art import text2art

Art=text2art("Scrapp",font='block',chr_ignore=True) # Return ASCII text with block font
print(Art)
print("""
Welcome to scrapp! This is a filtered-feed service, where you collect
and grow a personal knowledge store of information you trust. Content you upload can be consumed 
at variable levels of abstractions: small machine-generated summaries 
up to elaborate essays. Quotes can be automatically sourced, and we include
a Wayback Machine-like functionality that saves local copies of webpages 
in case they are edited or lost. Capable of internet searching for improved context. 
And perhaps most impressively and most challengingly, building a world model based on the first order proposition simplied from the text""")
print(
"""
What makes up a scrapp?"
A scrapp in our term for an individual piece of information in our collection.
It has the following qualities:
1) ATOMIC - conveys meaningful information on it's own if a dictionary is used.
2) CONTEXTUALIZED - contains important data about where the scrapp was sourced, when it was saved, authorship
""")


import pytholog as pl

# Create a new knowledge base
family_kb = pl.KnowledgeBase("family")

# Add facts (objects and propositions)
family_kb([
    "parent(john, mary)",
    "parent(john, tom)",
    "parent(jane, mary)",
    "parent(jane, tom)",
    "parent(mary, ann)",
    "parent(tom, peter)",
    "male(john)",
    "male(tom)",
    "male(peter)",
    "female(jane)",
    "female(mary)",
    "female(ann)"
])

# Add rules
family_kb([
    "father(X, Y) :- parent(X, Y), male(X)",
    "mother(X, Y) :- parent(X, Y), female(X)",
    "grandparent(X, Z) :- parent(X, Y), parent(Y, Z)",
    "sibling(X, Y) :- parent(Z, X), parent(Z, Y), neq(X, Y)"
])

# Query the knowledge base
print("Fathers:")
print(family_kb.query(pl.Expr("father(X, Y)")))

print("\nMothers:")
print(family_kb.query(pl.Expr("mother(X, Y)")))

print("\nParents of Ann:")
print(family_kb.query(pl.Expr("parent(X, ann)")))

print("\nSiblings:")
print(family_kb.query(pl.Expr("sibling(X, Y)")))

# Add a new fact
family_kb(["parent(ann, lisa)"])

print("\nGrandchildren of John:")
print(family_kb.query(pl.Expr("grandparent(john, X)")))