var store = new Vuex.Store({
    state: {
        posts: [],
        selectedPost: {
            "images": [],
            "tags": [],
            "title": null,
            "slug": "2020-05-31-0338170009330000",
            "content": "<p>Đời chỉ có một lần. Vậy nó sẽ phải làm gì?</p>",
            "created_on": "2020-05-31T10:38:17.037000+07:00"
        },
        loading: true,
        nextUrl: "/api/post-list/",
    },
    getters: {
        selectedPost(state) {
            return state.selectedPost;
        }
    },
    mutations: {
        loading(state) {
            state.loading = true;
        },
        selecPost(state, { post }) {
            state.selectedPost = post
        },
        appendPost(state, { posts, nextUrl }) {
            state.posts = state.posts.concat(posts);

            state.nextUrl = nextUrl;
            state.loading = false;
        }
    },
    actions: {
        loadPost(context) {
            if (!context.state.nextUrl) {
                console.log(" STOP next is null")
                return;
            }
            if (context.state.loading && context.state.posts.length) {
                console.log("STOP  it's loading")
                return;
            }
            context.commit('loading');
            $.ajax({
                url: context.state.nextUrl,
                success: function (res) {
                    console.log("next loaded:", res.next)
                    store.commit('appendPost', {
                        posts: res.results,
                        nextUrl: res.next
                    });
                }
            })
        },
        selectPost(context, post) {
            console.log("selected: ", post.title);
            context.commit("selecPost", { post: post });
        }
    }
});

PostList = Vue.component('post-list', {
    props: ['posts'],
    template: "#post-list-template",
    updated: function () {
        let magicGrid = new MagicGrid({
            container: '.container-post',
            animate: true,
            gutter: 15,
            static: true,
            useMin: true
        });

        magicGrid.listen();
    }
});

Post = Vue.component('post', {
    props: ["post"],
    template: "#post-template",
    mounted: function () {
        $(this.$el).find(".post-content").dotdotdot();
    },
    methods: {
        handleClick(event) {

            // if click tag -> don't open dialog            
            if (event.target.tagName == "SPAN" && event.target.className.includes('tag')) {
                return;
            }

            var my_date_format = function (input) {
                var d = new Date(input);
                var month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                var date = d.getDate() + " " + month[d.getMonth()] + ", " + d.getFullYear();
                var time = d.toLocaleTimeString().toLowerCase().replace(/([\d]+:[\d]+):[\d]+(\s\w+)/g, "$1$2");
                return (date + " " + time);
            };

            let selectedPost = this.post;
            selectedPost.created_on = my_date_format(selectedPost.created_on);
            this.$store.dispatch("selectPost", selectedPost);
            $('#myModel').modal('show');
        }
    }
});

PostDetail = Vue.component('post-detail', {
    props: ["selectedPost"],
    template: "#post-detail-template",
});

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    store,
    mounted: function () {

    },
    computed: {
        posts() {
            return store.state.posts
        },
        loading() {
            return store.state.loading
        },
        selectedPost() {
            return store.state.selectedPost
        }
    }
});

$('.post').click(function (event) {

});

store.dispatch('loadPost');


$(window).on("scroll", function () {
    var scrollHeight = $(document).height();
    var scrollPosition = $(window).height() + $(window).scrollTop();
    if ((scrollHeight - scrollPosition) / scrollHeight <= 0.2) {
        store.dispatch('loadPost');
    }
});