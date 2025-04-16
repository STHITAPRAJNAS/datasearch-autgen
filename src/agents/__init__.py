def create_empty_file(filepath):
    with open(filepath, 'w') as f:
        pass

create_empty_file("src/agents/__init__.py")
create_empty_file("src/utils/__init__.py")