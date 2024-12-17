import marimo

__generated_with = "0.9.9"
app = marimo.App(width="medium")


@app.cell
def __():
    from langchain_text_splitters import NLTKTextSplitter
    from maverick import Maverick
    import spacy
    from detokenize.detokenizer import detokenize
    from tqdm import tqdm
    from pprint import pprint
    import json

    import PyPDF2
    import ollama
    nlp_lg = spacy.load('en_core_web_lg')
    return (
        Maverick,
        NLTKTextSplitter,
        PyPDF2,
        detokenize,
        json,
        nlp_lg,
        ollama,
        pprint,
        spacy,
        tqdm,
    )


@app.cell
def __():
    text = """Mindfulness is in a cO*ategory all by itself, as it can potentially balance and perfect the remaining four spiritual faculties. This does not mean that we shouldn't like the other two pairs, but that mindfulness is extremely important. 
    Mindfulness means knowing what is as it is right now. It is the quality of mind that knows things as they are. Really, it is the quality of sensations manifesting as they are, where they are, and on their own. However, initially it appears to be something we create and cultivate, and that is okay for the time being."""
    x = """If you
    are trying to perceive the sensations that make up your experience clearly and to know what
    they are, you are balancing energy and concentration, and faith and wisdom. Due to energy, the
    mind is alert and attentive. Due to concentration, it is stable. Faith here may also mean acceptance, and wisdom here is clear comprehension.
    Notice that this has nothing to do with some vague spacing out in which we wish that reality
    would go away and our thoughts would never arise again. I don't know where people get the
    notion that vague and escapist aversion to experience and thought are related to insight practice, but it seems to be a common one. Mindfulness means being very clear about our human,
    mammalian reality as it is. It is about being here now. Truth is found in the ordinary sensations
    that make up our experience. If we are not mindful of them or reject them because we are looking for “progress”, “depth”, or “transcendence”, we will be unable to appreciate what they have
    to teach, and be unable to do insight practices.
    The five spiritual faculties have also been presented in another order that can be useful:
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

    #https://stackoverflow.com/questions/56977820/better-way-to-use-spacy-to-parse-sentences
    return text, x


@app.cell
def __(Maverick):
    model = Maverick(device='cuda')
    return (model,)


@app.cell
def __():
    def get_special_suffix(pronoun):
        """Return special suffix for certain pronouns, or None if no special handling needed"""
        reflexive_map = {
            'itself': '-self',
            'himself': '-self',
            'herself': '-self',
            'themselves': '-selves',
            'myself': '-self',
            'yourself': '-self',
            'yourselves': '-selves',
            'ourselves': '-selves'
        }

        possessive_map = {
            'his': "'s",
            'hers': "'s",
            'its': "'s",
            'theirs': "'s",
            'ours': "'s",
            'yours': "'s"
        }

        # Convert to lowercase for matching
        pronoun_lower = pronoun.lower()

        if pronoun_lower in reflexive_map:
            return reflexive_map[pronoun_lower]
        elif pronoun_lower in possessive_map:
            return possessive_map[pronoun_lower]
        return None

    def adjust_offset_for_newlines(text, offset):
        """Adjust character offset accounting for newlines in text"""
        newline_positions = [i for i, char in enumerate(text) if char == '\n']
        newline_count = sum(1 for pos in newline_positions if pos < offset)
        return offset - newline_count

    def replace_coreferences(text, clusters_token_offsets, clusters_char_offsets, clusters_token_text):
        """Replace coreferences in text with their original noun"""
        # Remove newlines for processing but keep original for reference
        text_no_newlines = text.replace("\n", "")

        # Create a list of replacements to make
        replacements = []

        for token_offsets, char_offsets, cluster_text in zip(
            clusters_token_offsets, 
            clusters_char_offsets, 
            clusters_token_text
        ):
            if not char_offsets:
                continue

            # Get the first mention (assumed to be the original noun)
            first_mention = text_no_newlines[char_offsets[0][0]:char_offsets[0][1] + 1]

            # Add all subsequent mentions to replacements
            for start, end, mention in zip(
                [x[0] for x in char_offsets[1:]], 
                [x[1] for x in char_offsets[1:]], 
                cluster_text[1:]
            ):
                # Check if this mention needs special handling
                suffix = get_special_suffix(mention)
                replacement = first_mention + (suffix if suffix else '')

                replacements.append((start, end + 1, replacement))

        # Sort replacements in reverse order to avoid offset issues
        replacements.sort(reverse=True)

        # Make the replacements
        result = text_no_newlines
        for start, end, replacement in replacements:
            result = result[:start] + replacement + result[end:]

        return result


    return (
        adjust_offset_for_newlines,
        get_special_suffix,
        replace_coreferences,
    )


@app.cell
def __():
    # model_out = model.predict(text)
    return


@app.cell
def __(model_out, replace_coreferences, text):

    processed_text = replace_coreferences(text, 
                                        model_out["clusters_token_offsets"],
                                        model_out["clusters_char_offsets"],
                                        model_out["clusters_token_text"])

    print(processed_text)
    return (processed_text,)


@app.cell
def __():
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered

    converter = PdfConverter(
        artifact_dict=create_model_dict(device='cuda'),
    )

    return PdfConverter, converter, create_model_dict, text_from_rendered


@app.cell
def __(converter, text_from_rendered):
    rendered = converter(r"C:\GH\ontogen\sandbox\documents\mctb2_3fact.pdf")
    ocr_text, _, images = text_from_rendered(rendered)
    return images, ocr_text, rendered


@app.cell
def __(ocr_text):
    ocr_text
    return


@app.cell
def __(ocr_text):
    from textsplitter import TextSplitter

    text_splitter = TextSplitter(
            max_token_size=300,
            end_sentence=True,
            preserve_formatting=False, #opposite is true?
            remove_urls=False,
            replace_entities=True,
            remove_stopwords=False,
            language="english",
        )

    text_chunks = text_splitter.split_text(ocr_text)
    print(text_chunks)

    for zx in text_chunks:
        print(zx)
        print("=" * 300)
        print("=" * 300)
    return TextSplitter, text_chunks, text_splitter, zx


@app.cell
def __():
    # IDEA
     # always running twitter bot that constantly pulls new research, process it and determiones promising research and promising directions of research
    return


if __name__ == "__main__":
    app.run()
