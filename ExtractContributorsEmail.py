from json import load, dump
import os


def load_json(filename):
    with open(filename, 'r') as f:
        return load(f)


def prepare_user(user):
    name = user['name']
    email = user['email']
    user_info = user['user']
    login = None
    user_name = None
    if not user_info:
        print('No user object found: ' + str(user))
    else:
        login = user_info['login']
        user_name = user_info['name']
    if not name or not email:
        print('Missing user attributes')
    return {'name': name, 'login': login, 'email': email, 'user_name': user_name}


def ensure_result_dir(result_dir):
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

def write_users(users, name, result_dir):
    ensure_result_dir(result_dir)

    with open(os.path.join(result_dir, name), 'w') as f:
        dump(users, f)


def write_emails(emails, name, result_dir):
    ensure_result_dir(result_dir)

    with open(os.path.join(result_dir, name), 'w') as f:
        for email in emails:
            f.write(email + str(os.linesep))


def extract_commit_user(repository_data, result_dir):
    commits = extract_committers(repository_data)
    commiters = []
    authors = []
    emails = []
    for commit in commits:
        committer = prepare_user(commit['committer'])
        author = prepare_user(commit['author'])
        if committer not in commiters:
            commiters.append(committer)
        if author not in authors:
            authors.append(author)
        if committer['email'] not in emails:
            emails.append(committer['email'])
        if author['email'] not in emails:
            emails.append(author['email'])
    write_users(commiters, 'committers.json', result_dir)
    write_users(authors, 'authors.json', result_dir)
    write_users(emails, 'emails.json', result_dir)
    write_emails(emails, 'emails.txt', result_dir)


def extract_committers(repository_data):
    default_branch_ref = repository_data['defaultBranchRef']
    if not default_branch_ref:
        return print_not_found('default_branch_ref')
    target = default_branch_ref['target']
    if not target:
        return print_not_found('target')
    history = target['history']
    if not history:
        print_not_found('history')
    nodes = history['nodes']
    if not nodes:
        print_not_found('nodes')
    return nodes


def print_not_found(name):
    print(name + ' not available.')
    return []


def extract_contributors_emails(filename, result_dir):
    data = load_json(filename)
    for repo in data:
        if data[repo]:
            extract_commit_user(data[repo], result_dir)


extract_contributors_emails('./data/resultMorphia/result.json', './result/morphia/')
extract_contributors_emails('./data/resultObjectify/result.json', './result/objectify/')

