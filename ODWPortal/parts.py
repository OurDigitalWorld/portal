from urllib import request
import json
# from Portal.customlog import log_request


def get_solr(url, output_format):
    # log_request('url (parts.7)', url)
    try:
        conn = request.urlopen(url)
        if output_format == "xml":
            rdata = []
            chunk = 'xx'
            while chunk:
                chunk = conn.read()
                if chunk:
                    rdata.append(chunk)
            str1 = rdata
        else:
            str_response = conn.read().decode('utf-8')
            str1 = json.loads(str_response)
        conn.close()
    except IOError:
        # print 'Cannot open <strong class="highlight">URL</strong> %s for reading' % url
        str1 = 'error!'
    if isinstance(str1, list):
        return_value = str1[0]
    else:
        return_value = str1
    return return_value
