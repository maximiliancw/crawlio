var app = new Vue({
    el: '#app',
    data() {
        return {
            loading: false,
            form: {
                url: '',
                selectors: [],
            },
            newSelector: { name: '', query: '' },
            rows: [],
            stats: {}
        }
    },
    methods: {
        isValidURL(str) {
            const regexp = /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;
            return regexp.test(str);
        },
        createSelector() {
            this.form.selectors.push(Object.assign({}, this.newSelector))
            this.newSelector = { name: '', query: '' }
        },
        deleteSelector(selector) {
            this.form.selectors = this.form.selectors.filter(s => s !== selector)
        },
        submit() {
            this.loading = true
            fetch('/api/crawl', {
                method: 'POST',
                body: JSON.stringify(this.form),
                headers: { 'Content-Type': 'application/json'}
            })
                .then(async (res) => {
                    let data = await res.json()
                    this.rows = data.data
                    this.stats = data.info
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