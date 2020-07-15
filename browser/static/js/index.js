var store = new Vuex.Store({
    state: {
        posts: [],
        selectedPost: {},
        initing: true,
        loading: true,
        nextUrl: "/api/posts/",
        searchKey: ""
    },
    getters: {
        selectedPost(state) {
            return state.selectedPost;
        }
    },
    mutations: {
        initing(state) {            
            state.initing = true;
        },
        loading(state) {            
            state.loading = true;
        },
        selectedPost(state, post) {
            state.selectedPost = post;
        },
        searchPost(state, key) {   
            state.initing = true;         
            state.posts = [];
            state.searchKey = key;
        },
        initPosts(state, { posts, nextUrl }) {
            state.posts = posts;
            state.nextUrl = nextUrl;
            state.loading = false;
            state.initing = false;
        },
        appendPost(state, { posts, nextUrl }) {
            state.posts = state.posts.concat(posts);

            state.nextUrl = nextUrl;
            state.loading = false;
        }
    },
    actions: {
        initPosts(context) {
            let url = "/api/posts/";
            url += context.state.searchKey ? "?search=" + context.state.searchKey : "";
            context.commit('loading');
            $.ajax({
                url: url,
                success: function (res) {
                    console.log("Inited, next url:", res.next);
                    store.commit('initPosts', {
                        posts: res.results,
                        nextUrl: res.next
                    });
                }
            })
        },
        loadPost(context) {
            if (!context.state.nextUrl) {
                console.log("STOP next is null");
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
                    console.log("LoadPost nexturl: ", res.next)
                    store.commit('appendPost', {
                        posts: res.results,
                        nextUrl: res.next
                    });
                }
            })
        },
        searchPost(context, key) {
            context.commit("searchPost", key);
            context.dispatch("initPosts");
        },
        selectPost(context, post) {
            context.commit("selectedPost", post);
        }
    }
});

PostList = Vue.component('post-list', {
    props: ['posts'],
    template: "#post-list-template",
    updated: function () {
        if ($(".container-post")) {
            let magicGrid = new MagicGrid({
                container: '.container-post',
                animate: true,
                gutter: 15,
                static: true,
                useMin: true
            });
    
            magicGrid.listen();
        }
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
            console.log("clicked tagName: ", event.target.tagName);
            if (event.target.tagName == "A" && event.target.className.includes('tag')) {
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
        store.dispatch('initPosts');
    },
    computed: {
        posts() {
            return store.state.posts
        },
        initing() {
            return store.state.initing
        },
        loading() {
            return store.state.loading
        },
        selectedPost() {
            return store.state.selectedPost
        }
    }
});



$(window).on("scroll", function () {
    var scrollHeight = $(document).height();
    var scrollPosition = $(window).height() + $(window).scrollTop();
    if ((scrollHeight - scrollPosition) / scrollHeight <= 0.2) {
        store.dispatch('loadPost');
    }
});


(function () {
    var timeout = {};
    var update = function () {
        clearTimeout(timeout);
        timeout = setTimeout(function () {
            var key = $('#search').val();            
            store.dispatch('searchPost', key);
        }, 1000);
    };

    $('input#search').keyup(update);
    $('input#search').change(update);
}());