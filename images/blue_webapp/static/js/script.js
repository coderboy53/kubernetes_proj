async function getIp() {
  // sends get request to IP, awaits response, then parses response into JSON, awaits parsing then prints the fetched Pod IP to alert bar 
  fetch("/getip").then((response) => response.json()).then((data) => window.alert("Other pod IP is: "+data.message))
}

// function to display form and get the data submitted in the form
async function getFormData(){
  return new Promise((resolve) => {
  let formData = {};
  const popup = window.open("/form","_blank", "popup,width=640,height=800");
  popup.onload = () => {
    const form = popup.document.getElementById('form');
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      formData.name = form.elements['name'].value;
      formData.time = form.elements['time'].value;
      formData.text = form.elements['text'].value;
      popup.close()
      resolve(formData);
    });
  };
});
}

// function storing data to ephemeral mount
async function saveData(){
  const formData = await getFormData();
  fetch('/save', {
    method: 'POST',
    body: JSON.stringify(formData),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then((response) => response.json()).then((data) => window.alert(data.message));
}

async function getData(){
  fileName = window.prompt('Enter the filename');
  const response = await fetch('/getsave/?fileName='+fileName);
  const result = await response.json()
  if (response.status == 404)
  {
    window.alert(result.detail)
  }
  else if (response.status == 200)
  {
    window.alert('Name: '+result.name+'\nTime: '+result.time+'\nText: '+result.text);
  }
  
}

// function storing data to persistent volume mount
async function saveVolume(){
  const formData = await getFormData();
  fetch('/savev', {
    method: 'POST',
    body: JSON.stringify(formData),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then((response) => response.json()).then((data) => window.alert(data.message));
}

async function getVolume(){
  fileName = window.prompt('Enter the filename');
  const response = await fetch('/getsavev/?fileName='+fileName);
  const result = await response.json()
  if (response.status == 404)
  {
    window.alert(result.detail)
  }
  else if (response.status == 200)
  {
    window.alert('Name: '+result.name+'\nTime: '+result.time+'\nText: '+result.text);
  }
  
}

// function to store data to DB
async function saveDB(){
  const formData = await getFormData();
  fetch('/saved', {
    method: 'POST',
    body: JSON.stringify(formData),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then((response) => response.json()).then((data) => window.alert('Name: '+data.name+'\nTime: '+data.time+'\nText: '+data.text));
}

async function getDB(){
  let time = window.prompt("Enter timestamp added during DB entry");
  const response = await fetch('/getd?time='+time);
  const body = await response.json();
  if (response.status == 404)
  {
    window.alert(body.detail);
  }
  else if (response.status == 200)
  {
    window.alert('Name: '+body.name+'\nTime: '+body.time+'\nText: '+body.text);
  }

}


window.addEventListener("load", async () => {
  let ip = document.getElementById('ip');
  fetch('/ip').then((response) => response.json()).then((data) => {ip.innerHTML = 'My IP: '+data.message})
})