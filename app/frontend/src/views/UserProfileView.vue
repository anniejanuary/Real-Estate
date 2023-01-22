<template>

  <section class="h-100 gradient-form">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-xl-10">
          <div class="card rounded-3 text-black">
            <div class="row g-0">
              <div class="col-lg-6">
                <div class="card-body p-md-5 mx-md-4">

                  <div class="text-center">
                    <!--TODO: provide custom webp logo file later on-->
                    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/lotus.webp"
                      style="width: 185px;" alt="logo">
                    <h4 class="mt-1 mb-5 pb-1">The Real Estate User Dashboard</h4>
                  </div>

                  <div class="text-center pt-1 mb-5 pb-1">
                    <div>
                      <p>Your username:</p>
                      <p>{{ user_data.name }}</p>
                    </div>
                    <div>
                      <p>Your email:</p>
                      <p>{{ user_data.email }}</p>
                    </div>

                    <div class="pt-1 mb-5 pb-1">
                      <button class="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3" type="button"
                        @click="getUserData()">Get Data</button>
                      <button class="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3" type="button"
                        @click="logOut()">Log Out</button>
                    </div>

                  </div>

                </div>
              </div>
              <div class="col-lg-6 d-flex align-items-center gradient-custom-2">
                <div class="text-white px-3 py-4 p-md-5 mx-md-4">
                  <h4 class="mb-4">Here You can find all your profile related data and settings.</h4>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

</template>

<script>
export default {
  data () {
    return {
      user_data: {}
    }
  },
  methods: {
    getUserData () {
      const requestOptions = {
        method: 'GET',
        headers: {
          'Content-type': 'application/json'
        },
        credentials: 'include'
      }

      fetch('http://127.0.0.1:8000/api/user/me/', requestOptions)
        .then(response => response.json())
        // eslint-disable-next-line no-return-assign
        .then(data => {
          this.user_data = data
        })
    },
    logOut () {
      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-type': 'application/json'
        },
        credentials: 'include'
      }

      fetch('http://127.0.0.1:8000/api/auth/logout/', requestOptions)

      window.location.href = '/#/home'
    },
    mounted () {
      this.getUserData()
    }
  }
}

</script>

<!--TODO move styles to separate file ?-->
<style scoped lang="scss">
.gradient-custom-2 {
  /* fallback for old browsers */
  background: #fccb90;

  /* Chrome 10-25, Safari 5.1-6 */
  background: -webkit-linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);

  /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
  background: linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);
}

@media (min-width: 768px) {
  .gradient-form {
    height: 90vh !important;
  }
}

@media (min-width: 769px) {
  .gradient-custom-2 {
    border-top-right-radius: .3rem;
    border-bottom-right-radius: .3rem;
  }
}
</style>
