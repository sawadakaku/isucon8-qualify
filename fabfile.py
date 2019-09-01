from fabric import task
import os.path
import glob
import re

@task
def deploy_webapp(c):
    # copy files under webapp/**/* to /home/isucon/torb/webapp
    lacal_files = c.run('git ls-files ./webapp').stdout.strip().split('\n')
    for local_file in local_files:
        if os.path.isdir(local_file):
            continue
        remote_file = os.path.join('/home/isucon/torb', local_file)
        if c.run('test -d {}'.format(os.path.dirname(remote_file)), warn=True).failed:
            c.run(f"mkdir -p {os.path.dirname(remote_file)}")
        c.put(local_file, remote_file)
    # copy files under db/**/* to /home/isucon/torb/webapp
    lacal_files = c.run('git ls-files ./db').stdout.strip().split('\n')
    for local_file in local_files:
        if os.path.isdir(local_file):
            continue
        remote_file = os.path.join('/home/isucon/torb', local_file)
        c.put(local_file, remote_file)

    # /etc files
    etc_files = [
        'h2o/default-h2o.conf',
        'systemd/system/torb.python.service',
        'systemd/system/multi-user.target.wants/h2o.service',
        'systemd/system/multi-user.target.wants/mariadb.service'
    ]

    for etc_file in etc_files:
        print("etc_file: ", etc_file)
        local_file = os.path.join('./etc', etc_file)
        remote_file = os.path.join('/home/isucon/torb/etc', etc_file)
        if c.run('test -d {}'.format(os.path.dirname(remote_file)), warn=True).failed:
            c.run(f"mkdir -p {os.path.dirname(remote_file)}")
        c.put(local_file, remote_file)
        src_file = os.path.join("/home/isucon/torb/etc", etc_file)
        dst_file = os.path.join("/etc", etc_file)
        print("src_file: ", src_file)
        print("dst_file: ", dst_file)
        if c.sudo('test -d {}'.format(os.path.dirname(dst_file)), warn=True).failed:
            c.sudo(f"mkdir -p {os.path.dirname(dst_file)}")
        c.sudo(f'cp {src_file} {dst_file}')

    c.run('cd /home/isucon/torb/webapp/python && bash -lc "sh setup.sh"')

    restart_db(c)
    restart_h2o(c)
    restart_webapp(c)

@task
def restart_db(c):
    c.sudo('systemctl enable mariadb')
    c.sudo('systemctl restart mariadb')

@task
def restart_h2o(c):
    c.sudo('systemctl enable h2o')
    c.sudo('systemctl restart h2o')

@task
def restart_webapp(c):
    c.sudo('systemctl enable torb.python')
    c.sudo('systemctl restart torb.python')

@task
def run_bench(c):
    c.run('cd /home/isucon/torb/bench && ./tools/do_bench.sh')
