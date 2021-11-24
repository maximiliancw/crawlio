let app = new Vue({
    el: '#app',
    data() {
        return {
            loading: false,
            form: {
                url: '',
                selectors: {},
            },
            newSelector: { name: '', query: '' },
            columns: [{}],
            rows: []
        }
    },
    methods: {
        addSelector() {
            this.form.selectors[this.newSelector.name] = this.newSelector.query
            this.newSelector = { name: '', query: '' }
        },
        delSelector(selector) {
            delete this.form.selectors[selector.name]
        },
        submit() {
            this.loading = true
            fetch('/crawl', { method: 'post', data: this.form })
                .then((res) => {
                    this.rows = res.json()
                    this.loading = false
                })
                .catch((err) => {
                    console.log(err)
                    this.loading = false
                })
        },
        download() {
            // TODO
        }
    }
});