import requests
import pandas
import json
import random



class GitHub:

    api_url = 'https://api.github.com/repos'
    hardcoded_repositories = [
        'DSAI'
    ]

    def __init__(self, username, token):
        self.username = username
        self.token = token
        self.database = dict()

        # Set some useful attributes for the API calls
        self.api_url += f'/{self.username}'
        self.headers = {
            'Accept'                :  'application/vnd.github+json',
            'Authorization'         : f'Bearer {self.token}',
            'X-GitHub-Api-Version'  :  '2022-11-28'
        }
        self.data = {
            'permission': 'push'
        }

        # Load the collaborators and repositories
        try:
            self.load_database()
        except FileNotFoundError as e:
            print('No database found!')
            print(f'Hardcoded repositories: {self.hardcoded_repositories}')
            print('Retrieving collaborators and repositories from GitHub...')
            self.database['users'] = []
            self.database['repositories'] = dict()
            self.build_database(self.hardcoded_repositories)
            self.save_database()
            print('Done!', 'Edit the database.json file to add new users!')
            print(f'To discover which are the repositories of the project please visit: https://github.com/GabrielePintus/DSAI')
        except Exception as e:
            print('Generic Error - Failed to load the database')
            print(e)

        

    # Load the repositories list from a file
    def load_database(self, filename="database.json"):
        with open(filename, 'r') as f:
            self.database = json.load(f)
        
    # Add a collaborator to a repository
    def add_collaborator_to_repo(self, collaborator='', repository=''):
        try:
            url = f'{self.api_url}/{repository}/collaborators/{collaborator}'
            r = requests.put(url, headers=self.headers, json=self.data)
            return r.status_code
        except Exception as e:
            # Generic error
            print('Generic Error - Failed to add ' + collaborator + ' to ' + repository)
            print(e)

    # Add a list of collaborators to a repository
    def add_collaborators_to_repo(self, collaborators=[], repository=''):
        for collaborator in collaborators:
            self.add_collaborator_to_repo(collaborator, repository)

    # Add all the collaborators to all the repositories
    def add_collaborators_to_repos(self):
        # Check which users are not collaborators of which repositories
        users = [user['username'] for user in self.database['users']]
        to_add = {}
        for repo in self.database['repositories']:
            diff = set(users) - set(self.database['repositories'][repo]['collaborators'])
            to_add[repo] = list(diff)
        
        # If there are no users to add, exit
        length = sum([ len(v) for v in to_add.values() ])
        if length == 0:
            print('No users to add!')
            return
        

        # Add the collaborators to the repositories and save the results
        for repo, collaborators in to_add.items():
            for collaborator in collaborators:
                code = self.add_collaborator_to_repo(collaborator, repo)
                if code == 201:
                    # Add the collaborator to the database
                    self.database['repositories'][repo]['collaborators'].append(collaborator)
                    print(f'Added {collaborator} to {repo}')
                elif code == 204:
                    # Check if the collaborator is already in the database
                    if collaborator not in self.database['repositories'][repo]['collaborators']:
                        self.database['repositories'][repo]['collaborators'].append(collaborator)
                        print(f'Added {collaborator} to {repo}')
                    print(f'{collaborator} is already a collaborator of {repo}')
                elif code == 404:
                    # Collaborator or repository not found
                    print(f'{collaborator} or {repo} not found')
                else:
                    # Generic error
                    print(f'Generic Error - Failed to add {collaborator} to {repo}')
        self.save_database()
    
    def retrieve_collaborators_of_repo(self, repository=''):
        try:
            url = f'{self.api_url}/{repository}/collaborators'
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return r.json()
            else:
                raise Exception('Failed to retrieve collaborators of ' + repository)
        except Exception as e:
            # Generic error
            print('Generic Error - Failed to retrieve collaborators of ' + repository)
            print(e)

    def build_database(self, repositories=[]):
        # Add the repositories to the database
        for repo in repositories:
            self.database['repositories'][repo] = {
                'collaborators': []
            }

        # Add the users to the database
        for repo in repositories:
            collaborators = []
            collaborators_response = self.retrieve_collaborators_of_repo(repo)

            for user in collaborators_response:
                # Do not consider the owner of the repository
                if user['login'] != self.username:
                    collaborators.append(user['login'])
        
            for collaborator in collaborators:
                if collaborator not in self.database['users']:
                    self.database['users'].append({
                        'username': collaborator,
                        'email': ''
                    })
                    self.database['repositories'][repo]['collaborators'].append(collaborator)
        
        # Save the database to a file
        self.save_database()


    # Save the database to a file
    def save_database(self, filepath='database.json'):
        with open(filepath, 'w') as f:
            json.dump(self.database, f, indent=4)


if __name__ == '__main__':
    USERNAME = ""
    TOKEN = ""
    # Create the GitHub object
    gh = GitHub(USERNAME, TOKEN)

    # Add the collaborators to the repositories
    gh.add_collaborators_to_repos()
