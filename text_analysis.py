import nltk

def tokenize_sentence(sentence):
    return nltk.word_tokenize(sentence)


# nltk.download('averaged_perceptron_tagger')  # Download tagger if needed

def pos_tagging(tokens):
    return nltk.pos_tag(tokens)

# from nltk.parse import stanford # You may need to install the Stanford Parser
# ... (set up the Stanford Parser, refer to NLTK documentation)

# def constituency_parse(sentence):
#     parser = stanford.StanfordParser() 
#     parse_trees = parser.parse(sentence.split())
#     for tree in parse_trees: 
#         tree.draw()  # Optionally visualize the tree


import spacy
nlp = spacy.load("en_core_web_sm")  # Load a spaCy model 

def dependency_parse(sentence):
    doc = nlp(sentence)

    # Collect the dependency relations as a list of tuples
    dependency_relations = [] 
    for token in doc:
        dependency_relations.append((token.text, token.dep_, token.head.text)) 

    return dependency_relations  # Return the list

def calculate_declarative_score(tagged_tokens, dependency_relations):
    score = 0
    if tagged_tokens[0][1].startswith('N'):  # Noun at the beginning
        score += 1
    for i in range(min(3, len(tagged_tokens))): # Check first few tokens
        if tagged_tokens[i][1].startswith('V'):  # Verb present
            score += 1
    for token, dep, head in dependency_relations:
        if dep == 'ROOT' and head == token: 
            score += 1 # Simple check for main subject-verb relation
    return score

def is_possibly_declarative(sentence):
    # ... (Your analysis code here)
    tokens = tokenize_sentence(sentence)
    tagged_tokens = pos_tagging(tokens)
    # constituency_parse(sentence)
    dependency_relations = dependency_parse(sentence)
    score = calculate_declarative_score(tagged_tokens, dependency_relations)
    threshold = 4  # You can adjust this
    return score >= threshold