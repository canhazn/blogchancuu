var store = new Vuex.Store({
    state: {
        posts: [],
        selectedPost: {},
        initing: true,
        loading: true,
        nextUrl: "/api/posts/",
        searchKey: "",
        querys: {
            search: "",
            tags: ""
        }
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
        filterPost(state, querys) {
            state.initing = true;
            state.posts = [];
            let key = querys.search ? querys.search : "";
            state.querys = querys;
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
        },
        likePost(state, {post}) {

        }
    },
    actions: {
        initPosts(context) {
            let url = "/api/posts/";
            url += context.state.querys.search ? "?search=" + context.state.querys.search : "";
            url += context.state.querys.tags ? "?tags=" + context.state.querys.tags : "";
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
            });
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
        likePost(context) {           
            if (context.state.loading && context.state.posts.length) {
                console.log("STOP  it's loading")
                return;
            }
            
            $.ajax({
                url: `/api/like-post/${context.post.slug}`,
                success: function (res) {
                    console.log("LoadPost nexturl: ", res.next)
                    store.commit('appendPost', {
                        posts: res.results,
                        nextUrl: res.next
                    });
                }
            })
        },
        filterPost(context, querys) {
            context.commit("filterPost", querys);
            context.dispatch("initPosts");
        },
        selectPost(context, post) {
            context.commit("selectedPost", post);
        }
    }
});

let magicGrid;

PostList = Vue.component('post-list', {
    props: ['posts'],
    template: "#post-list-template",
    mounted: function () {
        // Load post when scrolled to the the bottom
        $(window).on("scroll", function () {
            var scrollHeight = $(document).height();
            var scrollPosition = $(window).height() + $(window).scrollTop();
            if ((scrollHeight - scrollPosition) / scrollHeight <= 0.2) {
                store.dispatch('loadPost');
            }
        });
    },
    updated: function () {
        if ($(".container-post")) {
            magicGrid = new MagicGrid({
                container: '.container-post',
                animate: true,
                gutter: 15,
                static: true,
                useMin: true
            });
            magicGrid.listen();
            console.log("Post list updated");
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
            console.log("clicked tagName: ", this.post);
            if (event.target.tagName == "SPAN" && event.target.className.includes('tag')) return;

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
    updated: function () {
        console.log("post detail")
    }
});

PostImages = Vue.component('post-images', {
    props: ["images"],
    template: "#post-images-template",
    mounted: function () {
        if (!$(this.$el).find("img")) return;
        $(this.$el).find("img").each(function (index, element) {
            $(element).on('load', function () {
                magicGrid.positionItems()
            });
        });
    }
});


PostTitle = Vue.component('post-title', {
    props: ["title"],
    template: "#post-title-template"
});


PostContent = Vue.component('post-content', {
    props: ["content"],
    template: "#post-content-template"
});


PostTag = Vue.component('post-tag', {
    props: ["tag"],
    template: "#post-tag-template",
    methods: {
        handleClick(event) {
            if (event.target.innerText !== this.tag.title) return;
            store.dispatch('filterPost', { "tags": this.tag.id });
            $('#myModel').modal('hide');
        }
    }
});

LoadingIcon = Vue.component('loading-icon', {
    props: ["loading"],
    template: "#loading-icon-template"
});


var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    store,
    components: {
        'top-nav': window.httpVueLoader(STATIC_URL + "js/components/TopNav.vue"),
        'app-world': window.httpVueLoader(STATIC_URL + "js/components/AppWorld.vue")
    },
    mounted: function () {
        store.dispatch('initPosts');
        console.log(STATIC_URL)
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
