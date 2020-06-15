var store = new Vuex.Store({
    state: {
        posts: [],
        loading: true,
        nextUrl: "/api/post-list",
    },
    mutations: {
        loading(state) {
            state.loading = true;
        },
        appendPost(state, { posts, nextUrl}) {            
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
        $(".post-content").dotdotdot();
        // $(this.$el).find(".post-images").each(function() {
        //     var img = new Image();
        //     img.onload = function() {
        //         console.log($(this).attr('src') + ' - done!');
        //     }
        //     img.src = $(this).attr('src');
        // })
    }
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
        }
    }
});

$('.post').click(function (event) {
    let slug = $(this).data().postSlug;

    if (!event.target.className.includes('tag')) {
        window.location.href = slug
    }
});

store.dispatch('loadPost');


$(window).on("scroll", function () {
    var scrollHeight = $(document).height();
    var scrollPosition = $(window).height() + $(window).scrollTop();
    if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
        
        store.dispatch('loadPost');

    }
});