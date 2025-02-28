new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue.js!',
        inputData: '',
        responseMessage: ''
    },
    methods: {
        fetchData() {
            axios.get('/api/get_data')
                .then(response => {
                    this.message = response.data.message;
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        },
        postData() {
            axios.post('/api/post_data', { data: this.inputData })
                .then(response => {
                    this.responseMessage = response.data.message;
                })
                .catch(error => {
                    console.error('Error posting data:', error);
                });
        }
    }
});
