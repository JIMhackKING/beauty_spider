import requests
import io


def get_token(data):
    url = 'http://{host}/api2/auth-token/'.format(host=host)
    res = requests.post(url, data=data)
    res.raise_for_status()
    return res.json()


def get_upload_link(token, repo_id):
    url = 'http://{host}/api2/repos/{repo_id}/upload-link/'.format(host=host, repo_id=repo_id)
    res = requests.get(
        url, headers={'Authorization': 'Token {token}'.format(token=token)}
    )
    res.raise_for_status()
    return res.json()


def list_libs(token):
    url = 'http://{host}/api2/repos/'.format(host=host)
    res = requests.get(
        url, headers={'Authorization': 'Token {token}'.format(token=token)}
    )
    res.raise_for_status()
    return res.json()


def upload_file(upload_link, fp, parent_dir='/'):
    if isinstance(fp, io.IOBase):
        data = {'filename': fp.name.split('/')[-1], 'parent_dir': parent_dir}
        files = {'file': fp}
    elif isinstance(fp, str):
        data = {'filename': fp.split('/')[-1], 'parent_dir': parent_dir}
        files = {'file': open(fp, 'rb')}
    else:
        raise TypeError("fp type is invalid.")
    res = requests.post(upload_link, data=data, files=files)
    res.raise_for_status()
    return res.text


def create_dir(token, repo_id, dir_name):
    url = "http://{host}/api2/repos/{repo_id}/dir/".format(host=host, repo_id=repo_id)
    data = dict(operation="mkdir")
    params = {"p": dir_name if dir_name.startswith("/") else "/"+dir_name}
    headers = {'Authorization': 'Token {token}'.format(token=token)}
    res = requests.post(url, data=data, params=params, headers=headers)
    res.raise_for_status()
    return res.text


def get_dir(token, repo_id, dir_name):
    url = "http://{host}/api/v2.1/repos/{repo_id}/dir/detail/".format(host=host, repo_id=repo_id)
    headers = {'Authorization': 'Token {token}'.format(token=token)}
    params = {"path": dir_name}
    res = requests.get(url, headers=headers, params=params)
    return res.json()


if __name__ == '__main__':
    host = 'www.vmnas.com:8000'
    token = get_token({'username': 'a@a.com', 'password': '1'})
    token = token['token']
    libs = list_libs(token)
    for lib in libs:
        if lib.get('name') == "私人资料库":
            repo_id = lib.get('id')
            break
    else:
        repo_id = ''
    # upload_link = get_upload_link(repo_id, token)
    # print(upload_file(upload_link, 'test.py'))
    print(get_dir(token, repo_id, "test"))
