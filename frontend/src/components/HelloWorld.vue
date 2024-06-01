<template>
  <div>
    {{hello}}
  </div>
</template>

<script>

export default {
  name: 'hello',
  methods: {
    getHello () {
      fetch("http://localhost:8000/api/v1/connection/hello")
        .then(res => {
          return res.json()
        })
        .then(data => {
          this.hello = data
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  created () {
    this.getHello()
  },
  data () {
    return {
      hello: ""
    }
  }
}
</script>

