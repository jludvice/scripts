__author__ = 'jludvice'

'''
script for alignig RBAC roles in Fuse/Fabric8 repo
'''

import glob
import fileinput
import sys


rel_paths_fabric = (
    'fabric/fabric8-karaf/src/main/resources/etc/jmx.acl.*',
    'fabric/fabric8-karaf/src/main/resources/distro/fabric/import/fabric/profiles/acls.profile/jmx.acl.*',
    'fabric/fabric8-karaf/src/main/resources/distro/fabric/import/fabric/profiles/insight/elasticsearch.node.profile/jmx.acl.*',
    'tooling/rh-support/support-profiles/src/main/resources/fabric/import/fabric/profiles/support/base.profile/jmx.acl.*',
)

rel_paths_fuse = (
    'esb/shared/src/main/resources/etc/auth/jmx.acl.*',
    'mq/mq-assembly/shared/src/main/resources/etc/auth/jmx.acl.*',
)


base_path = '/path/to/git/repo/with/fabric8'
rel_paths = rel_paths_fabric

equal_roles = ('viewer', 'Monitor', 'Operator', 'Maintainer')
# equal_roles = ('Administrator', 'SuperUser', 'admin')
# equal_roles = ('Deployer', 'Auditor')


def any_role_in_string(text='', roles=equal_roles):
    '''
    return true if any role missing in text

    :param text: string to check
    :param roles: roles wich should be there
    :return: true if at least one role is in string
    '''
    return any(role in text for role in roles)


def all_equal_roles_in_string(text='', roles=equal_roles):
    '''
    returns true if all roles are in text

    :param text: text to check
    :param roles: roles which should be present
    :return: true if all roles are there
    '''
    return all(role in text for role in roles)


def append_if_missing(text='', roles=equal_roles):
    '''
    append roles which are missing in text

    :param text: line
    :param roles: list of roles
    :return: line with appended roles (and newline)
    '''
    append_roles = [role for role in roles if role not in text]

    if len(append_roles) > 0:
        # rstrip - if there is newline, strip (don't want newline inside string :)
        return "%s, %s\n" % (text.rstrip(), ", ".join(append_roles))

    return text


file_paths = []
for p in rel_paths:
    file_paths.extend(glob.glob(base_path + "/" + p))

for file_path in file_paths:

    # pipe stdin/stdout from/to given file
    for line in fileinput.input(file_path, inplace=True):
        # if line contains at elast one given role and not all of them
        # append missing
        if not line.startswith('#') and any_role_in_string(text=line) and not all_equal_roles_in_string():
            # use write instead of print to avoid duplicate newline
            sys.stdout.write(append_if_missing(text=line))

        else:
            sys.stdout.write(line)
