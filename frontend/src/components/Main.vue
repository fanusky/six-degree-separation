<template>
  <div>
    <h1>Introduce two actors:</h1>
    <div class="container">
      <div class="search-wrapper left" v-if="!movie1Selected">
        <h2>Actor 1</h2>
        <input type="text" v-model="leftInput" placeholder="Search actors..." />
        <div  v-if="!movie1Selected" class="item fruit" v-for="actor in filtered(leftInput, 1)" :key="actor" @click="selectMovie1(actor)">
          <p>{{ actor }}</p>
        </div>
        <div class="item error" v-if="leftInput && !filtered(leftInput, 1).length">
          <p>No results found!</p>
        </div>
      </div>
      <div v-else>
        <h2>Actor 1</h2>
        <h4>{{actor1}}</h4>
      </div>
      <div class="search-wrapper right" v-if="!movie2Selected">
        <h2>Actor 2</h2>
        <input type="text" v-model="rightInput" placeholder="Search actors..." />
        <div  v-if="!movie2Selected" class="item fruit" v-for="actor in filtered(rightInput, 2)" :key="actor" @click="selectMovie2(actor)">
          <p>{{ actor }}</p>
        </div>
        <div class="item error" v-if="rightInput && !filtered(rightInput, 2).length">
          <p>No results found!</p>
        </div>
      </div>
      <div v-else>
        <h2>Actor 2</h2>
        <h4>{{actor2}}</h4>
      </div>
    </div>
    <div v-if="!clicked" >
      <button @click="connect" class="custom-button">Connect!</button>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
    <div>
      <div v-for="(movie, index) in movies_connected" class="actor-connection">
        <div class="actor-pair">
          <div class="actor-card">
            <h3>{{actors_connected[index]}}</h3>
          </div>
          <div class="movie-title">
            <h4>{{movie}}</h4>
          </div>
          <div class="actor-card">
            <h3>{{actors_connected[index + 1]}}</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'Main',
  created () {
    if (localStorage.movies_connected) {
      let moviesJSON = localStorage.getItem('movies_connected')
      if (moviesJSON) {
        try {
          this.movies_connected = JSON.parse(moviesJSON)
        } catch (error) {
        }
      }
    }
    if (localStorage.actors_connected) {
      let actorsJSON = localStorage.getItem('actors_connected')
      if (actorsJSON) {
        try {
          this.actors_connected = JSON.parse(actorsJSON)
        } catch (error) {
        }
      }
    }
  },
  data() {
    return {
      leftInput: "",
      rightInput: "",
      movie1Selected: false,
      movie2Selected: false,
      actor1: "",
      lastActor1: "",
      lastActor2: "",
      actor2: "",
      movies_connected:[],
      actors_connected:[],
      filtered1: [],
      filtered2: [],
      clicked: false
    };
  },
  methods: {
    async searchName(name, num) {
      if(num == 1 && this.leftInput !== this.lastActor1 || num == 2 && this.rightInput !== this.lastActor2){
        try {
          const response = await fetch(`http://localhost:8000/api/v1/connection/actors/${name}`);
          const data = await response.json();

          if(data) {
            const actors = data.map(actor => actor[0]);
            if (num === 1){
              this.filtered1 = actors;
              this.lastActor1 = this.leftInput
            }
            else{
              this.filtered2 = actors;
              this.lastActor2 = this.rightInput
            }
          }

        } catch (error) {
          console.error(error);
          return [];
        }
      }
    },
    filtered(input, num) {
      this.searchName(input, num)
      if (num === 1){
        return this.filtered1
      }
      return this.filtered2
    },
    async getConnection() {
      try {
        const url = new URL("http://localhost:8000/api/v1/connection/connection"); // Replace with your backend URL
        url.searchParams.set('start', this.actor1);
        url.searchParams.set('end', this.actor2);

        const response = await fetch(url.toString(), {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json', // May be required by your backend
          },
        });

        if (!response.ok) {
          throw new Error(`Error fetching connection data: ${response.statusText}`);
        }

        const data_ret = await response.json();
        localStorage.setItem('actors_connected', JSON.stringify(data_ret.actors))
        localStorage.setItem('movies_connected', JSON.stringify(data_ret.movies))
        console.log("ret")
        console.log(this.actors_connected)
      } catch (error) {
        console.error('Error fetching connection data:', error);
        error.value = 'Failed to fetch connection data. Please try again.';
      } finally {
      }
    },
    selectMovie1(movie) {
      this.movie1Selected = true
      this.actor1 = movie
    },
    selectMovie2(movie) {
      this.movie2Selected = true
      this.actor2 = movie
    },
    async connect() {
      if(this.actor1 !== "" && this.actor2 !== ""){
        this.clicked = true
        await this.getConnection()
        this.$forceUpdate();
        location.reload()
      }
    }
  }
};
</script>
<style>
@import url("https://fonts.googleapis.com/css2?family=Montserrat&display=swap");

* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-family: "Montserrat", sans-serif;
}

body {
  padding: 20px;
  min-height: 100vh;
  background-color: rgb(234, 242, 255);
}

input {
  display: block;
  width: 350px;
  margin: 20px auto;
  padding: 10px 45px;
  background-size: 15px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
  rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
}

.item {
  width: 350px;
  margin: 0 auto 10px auto;
  padding: 10px 20px;
  color: white;
  border-radius: 5px;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 3px 0px,
  rgba(0, 0, 0, 0.06) 0px 1px 2px 0px;
}

.fruit {
  background-color: rgb(97, 62, 252);
  cursor: pointer;
}

.error {
  background-color: tomato;
}
.container {
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: space-evenly;
  width: 100vw;
}
.actor-connection {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f5f5f5;
}

.actor-pair {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actor-card {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  margin: 5px;
  text-align: center;
}

.movie-title {
  text-align: center;
  font-weight: bold;
  margin: 0 10px;
}
.custom-button {
  display: block;
  width: 350px;
  margin: 20px auto;
  padding: 10px 45px;
  background-size: 15px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
  rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
  cursor: pointer;
  text-align: center;
  color: black;
}
.custom-button:active {
  background-color: #2980b9; /* Clicked color */
}
</style>

