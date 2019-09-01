from fabric import task
import os.path

@task
def deploy_webapp(c):
    # copy files under webapp/**/* to /home/isucon/torb/webapp
    for local_file in glob.glob('./webapp/**/*', recursive=True):
        remote_file = re.sub('^\.', '/home/isucon/torb', local_file)
        c.put(local_file, remote_file)

    # copy files under db/**/* to /home/isucon/torb/webapp
    for local_file in glob.glob('./db/**/*', recursive=True):
        remote_file = re.sub('^\.', '/home/isucon/torb', local_file)
        c.put(local_file, remote_file)

    # /etc files
    etc_files = [
        'h2o/default-h2o.conf',
        'systemd/system/torb.python.service',
        'systemd/system/multi-user.target.wants/h2o.service',
        'systemd/system/multi-user.target.wants/mariadb.service'
    ]

    for etc_file in etc_files:
        c.put(os.path.join('./etc', etc_file), os.path.join('/home/isucon/etc', etc_file))
        c.sudo('cp {os.path.join("/home/isucon/etc", etc_file)} {os.path.join("/etc", etc_file)}')

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
