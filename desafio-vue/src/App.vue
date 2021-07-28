
<template>
<div id="app">
  <h2> Vue.js WebSocket Test </h2>
  <div id="corridas">
    <h1>Corrida de cavalos</h1>
  </div>
</div>
</template>

<script>
export default {
  name: 'App',
  data: function() {
    return {
      connection: null
    }
  },
  created: function() {
    console.log("Iniciando conexão com servidor WebSocket");
    this.connection = new WebSocket("ws://localhost:8000");

    function generateRandomLetter() {
      let alphabet = "abcdefghijklmnopqrstuvwxyz"

      return alphabet[Math.floor(Math.random() * alphabet.length)]
    }

    this.connection.onmessage = function(event) {

      const json_data = JSON.parse(event.data);

      if(json_data[0] == "largada") {
        let horseCount = json_data[1].length;
        var horse = [];
        let horses_div = document.createElement("div");
        horses_div.setAttribute("id", "cavalos");
        let div_cavalos = document.getElementById("corridas");
        div_cavalos.appendChild(horses_div);

        for (let i=0; i < horseCount; i++) {
          horse[i] = document.createElement("button");
          horse[i].setAttribute("id", `cavalo${i+1}`);
          horse[i].innerHTML = generateRandomLetter();
          horses_div.appendChild(horse[i]);
        }
      }

      if(json_data[0] == "update") {
        let i = 0;
        let horseCount = json_data[1].length;
        let horse = [];
        for(let lap of json_data[1].values()) {
          for (let j=0; j < horseCount; j++) {
            horse[j] = document.getElementById(`cavalo${j+1}`);
          }
          let value = lap.distancia*2;
          if(horse[i]) {
              horse[i].style.left = `${value}px`;
              horse[i].onclick = function() {
                alert(lap.nome);
              }
          }
          i++;
        }
      }
      if(json_data[0] == "vitoria") {
        alert(`${json_data[1].nome} venceu a corrida!`);
        let horses_div = document.getElementById('cavalos');
        if(horses_div) horses_div.remove();
      }

    }

    this.connection.onopen = function(event) {
      // console.log(event)
      console.log("Conectado ao servidor WebSocket com sucesso")
    }
  }
}
</script>

<style>
@import './assets/styles/balloon.css'
* {
	margin: 0;
	padding: 0;
	border: 0;
	font-size: 100%;
	font: inherit;
	vertical-align: baseline;
  box-sizing: border-box;
}

#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #3A3A3A;
  margin-top: 1em;
  justify-content: center;
}

#corridas {
  margin-top: 100px;
  width: 100%;
  height: 100px;
  background-color: #e67e22;
}

#corridas h1 {
  font-size: 2em;
}

#cavalos {
  width: 230px;
  height: 30px;
  background-color: #CCC;
  border-radius: 15px;
}

#cavalos button {
  position: absolute;
  display: block;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
}
</style>
