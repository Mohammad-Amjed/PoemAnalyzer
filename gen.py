import pkg_resources

with open('requirements.txt', 'w') as f:
    for dist in pkg_resources.working_set:
        req = dist.as_requirement()
        f.write(str(req) + '\n')
