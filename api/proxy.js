const fetch = require('node-fetch');

module.exports = async (req, res) => {
  const url = 'http://159.223.132.128:8080'; // Replace with the URL of the website you want to proxy

  try {
    const response = await fetch(url);
    const data = await response.text();

    res.setHeader('Content-Type', 'text/html');
    res.send(data);
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
};
