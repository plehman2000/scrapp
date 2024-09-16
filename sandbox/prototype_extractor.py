
from langchain_text_splitters import NLTKTextSplitter
from maverick import Maverick

text = """Mindfulness is in a category all by itself, as it can potentially balance and perfect the remaining four spiritual faculties. This does not mean that we shouldn't be informed by the other two pairs, but that mindfulness is extremely important. 
Mindfulness means knowing what is as it is right now. It is the quality of mind that knows things as they are. Really, it is the quality of sensations manifesting as they are, where they are, and on their own. However, initially
it appears to be something we create and cultivate, and that is okay for the time being.4
 If you
are trying to perceive the sensations that make up your experience clearly and to know what
they are, you are balancing energy and concentration, and faith and wisdom. Due to energy, the
mind is alert and attentive. Due to concentration, it is stable. Faith here may also mean acceptance, and wisdom here is clear comprehension.
Notice that this has nothing to do with some vague spacing out in which we wish that reality
would go away and our thoughts would never arise again. I don't know where people get the
notion that vague and escapist aversion to experience and thought are related to insight practice, but it seems to be a common one. Mindfulness means being very clear about our human,
mammalian reality as it is. It is about being here now. Truth is found in the ordinary sensations
that make up our experience. If we are not mindful of them or reject them because we are looking for “progress”, “depth”, or “transcendence”, we will be unable to appreciate what they have
to teach, and be unable to do insight practices.
The fve spiritual faculties have also been presented in another order that can be useful:
faith, energy, mindfulness, concentration, and wisdom. In this order, they apply to each of the
three trainings, the frst of which, as discussed earlier, is morality. We have faith that training
in morality is a good idea and that we can do it, so we exert energy to live up to a standard of
clear and skillful living. We realize that we must pay attention to our thoughts, words, and
deeds in order to do this, so we try to be mindful of them. We realize that we often fail to pay
attention, so we try to increase our ability to concentrate on how we live our life. In this way,
through experience, we become wiser in a relative sense, learning how to live a good and useful life. Seeing our skill improve and the benefts it has for our life, we generate more faith,
and so on.
With respect to training in concentration, we may have faith that we might be able to attain
high states of consciousness, so we sit down on a cushion and energetically try to stabilize our
attention and tune in to skillful qualities. We realize that we cannot stabilize our attention without mindfulness of our object and of the qualities of the state we wish attain. We develop strong
concentration by consistently stabilizing our attention. We attain high states of concentration
and thus gain a direct understanding of how to navigate in that territory and the meaning and
purpose of doing so. Our success creates more faith, and so we apply energy to further develop
our concentration abilities.
With the faith borne of the experience yielded by strong concentration, we begin to think it
might be possible to awaken, so we energetically explore all the sensations that make up our
world. With an alert and energetic mind, we mindfully explore this heart, mind, and body just
as it is now. Reality becomes more and more interesting, so our concentration grows, and this
combination of the first four produces fundamental wisdom. Wisdom leads to more faith, and
the cycle goes around again.    """
import spacy

model = Maverick(device='cuda')
nlp_lg = spacy.load('en_core_web_lg')


def get_best_noun(cluster, offsets): #gets best Noune from a cluster, if all pronoiuns return none
    ls = []
    for noun, offset in zip(cluster, offsets):
        pos = nlp_lg(noun)[0].pos_
        if pos in ["DET", "PROPN"]:
            ls.append([noun, offset])

    if len(ls) == 0:
        return None, None
    

    #TODO need better heuristic here, just picks first, should be informed by prior selections (search db for terms, select ones that are the same?)

    return ls[0][0], ls[0][1]


#https://stackoverflow.com/questions/56977820/better-way-to-use-spacy-to-parse-sentences
def get_pro_nsubj(token):
    # get the (lowercased) subject pronoun if there is one
    pro_nsubj_list = [child for child in token.children if child.dep_ == 'nsubj'] 
    if len(pro_nsubj_list) == 0:
        return None
    return pro_nsubj_list[0]


def get_declarations(doc):
    incomplete_facts = []
    for token in doc:
        if token.pos_ in ['NOUN', 'ADJ']:
            if token.dep_ in ['attr', 'acomp'] and token.head.lower_ in ['is', 'was',]: #TODO MAKE MORE ALL_ENCOMPASSING, probably use nested for loops? should apply to has, was etc
                # to test for lemma 'be' use token.head.lemma_ == 'be'
                nsubj = get_pro_nsubj(token.head)
                if nsubj:
                    # get the text of each token in the constituent and join it all together
                    factoid =  [nsubj," " + token.head.lower_ + " "+ ' '.join([t.text for t in token.subtree])]
                    incomplete_facts.append(factoid)
    return incomplete_facts




from detokenize.detokenizer import detokenize
from tqdm import tqdm

text = text.replace("\n\n", "")
text = text.replace("\n", " ")
text_splitter = NLTKTextSplitter(chunk_size=1000)
chunks = text_splitter.split_text(text)


all_facts = {}
for chunk in tqdm(chunks):
    pronoun_results = model.predict(chunk)
    pron_tokenized = pronoun_results['tokens']
    offs_to_pron = {}
    for i,(clusters, offsets) in enumerate(zip(pronoun_results['clusters_token_text'], pronoun_results['clusters_token_offsets'])):
        best_noun, best_noun_offset = get_best_noun(clusters, offsets)

        if best_noun != None:
            # print("\nBEST NOUN")
            # print(best_noun, best_noun_offset)
            # map all offsets to best_noun   
            for cl, off in zip(clusters, offsets):
                offs_to_pron[off[0]] = best_noun

    detokenized_chunk= detokenize(pron_tokenized)
    doc = nlp_lg(detokenized_chunk)
    tokens = [token for token in doc]


    incomplete_facts = get_declarations(tokens)

    # Merge common Nouns
    if incomplete_facts:
        for fact in incomplete_facts:
            word2match = fact[0]
            word2match_idx = fact[0].i
            if word2match_idx in offs_to_pron: # if there is a valid Noun to replace the pronoun with
                # print(word2match, word2match_idx,offs_to_pron[word2match_idx])
                pron_tokenized[word2match_idx] = offs_to_pron[word2match_idx]
                nu_noun = offs_to_pron[word2match_idx]
                if nu_noun not in all_facts:
                    all_facts[nu_noun] = []
                all_facts[nu_noun].append(fact[1])


print(all_facts)