async function getIp() {
  // sends get request to IP, awaits response, then parses response into JSON, awaits parsing then prints the fetched Pod IP to alert bar 
   fetch("http://127.0.0.1:8000/getip").then((response) => response.json()).then((data) => window.alert("Other pod IP is: "+data.message))
}