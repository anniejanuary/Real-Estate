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
                                        <h4 class="mt-1 mb-5 pb-1">The Real Estate register service</h4>
                                    </div>

                                    <form>
                                        <p>Register a new user account</p>

                                        <div class="form-outline mb-4">
                                            <input type="username" v-model="username" id="form2Example11"
                                                class="form-control" placeholder="Username" />
                                            <label class="form-label" for="form2Example11">Username</label>
                                        </div>

                                        <div class="form-outline mb-4">
                                            <input type="email" v-model="email" id="form2Example22" class="form-control"
                                                placeholder="Email" />
                                            <label class="form-label" for="form2Example11">Email</label>
                                        </div>

                                        <div class="form-outline mb-4">
                                            <input type="password" v-model="password" id="form2Example23"
                                                class="form-control" placeholder="Password" />
                                            <label class="form-label" for="form2Example22">Password</label>
                                        </div>

                                        <div class="pt-1 mb-5 pb-1">
                                            <button class="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3 me-1"
                                                type="button" @click="submit()">Create profile</button>
                                            <button class="btn btn-primary btn-block fa-lg gradient-custom-2 mb-3 me-1"
                                                type="button" @click="$router.go(-1)">Take me back</button>
                                        </div>

                                    </form>

                                </div>
                            </div>
                            <div class="col-lg-6 d-flex align-items-center gradient-custom-2">
                                <div class="text-white px-3 py-4 p-md-5 mx-md-4">
                                    <h4 class="mb-4">You are on the good way for your new place.</h4>
                                    <p class="small mb-0">Notifications and wishlisit on it's way.</p>
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
      email: '',
      password: ''
    }
  },
  methods: {
    submit () {
      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ name: this.username, email: this.email, password: this.password })
      }

      fetch('http://127.0.0.1:8000/api/user/create/', requestOptions)
        .then(result => result.json())
        .then(window.location.href = '/#/login')
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
