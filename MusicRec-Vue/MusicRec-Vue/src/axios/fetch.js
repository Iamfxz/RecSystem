import axios from './axios'
//A querystring parsing and stringifying library with some added security.
const qs = require('qs');

export default async(url = '', data = {}, type = 'GET', headers) => {
  type = type.toUpperCase();
  if (type === 'GET') {
    if (Object.keys(data).length !== 0) {
      url = url + '?' + qs.stringify(data);
    }
    //console.log(data)
  }
  let requestConfig = {
    method: type,
    headers: headers || {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Set-Cookie': 'widget_session=abc123; SameSite=None; Secure'
    }
  };

  if (type === 'POST') {
    requestConfig.data = qs.stringify(data);
    // console.log(requestConfig.data)
  }

  const response = await axios(url, requestConfig);
  if (response) {
    return response.data;
  }
}
