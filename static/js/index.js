var store = new Vuex.Store({
    state: {
        posts: []
    },
    mutations: {
        appendPost(state, posts) {
            state.posts = state.posts.concat(posts);
            console.log("get muta: ", state.posts)
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
        }
    }
});

$('.post').click(function (event) {
    let slug = $(this).data().postSlug;

    if (!event.target.className.includes('tag')) {
        window.location.href = slug
    }
});

nextUrl = "http://127.0.0.1:8000/api/post-list/?limit=3&offset=3";
$.ajax({
    url: "/api/post-list",
    success: function (res) {
        store.commit('appendPost', res.results);
        nextUrl = res.next;
    }
})

$(window).on("scroll", function () {
    var scrollHeight = $(document).height();
    var scrollPosition = $(window).height() + $(window).scrollTop();
    if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
        console.log('post list update');
        $.ajax({
            url: nextUrl,
            success: function (res) {
                if (!res.results) return;
                store.commit('appendPost', res.results);
                nextUrl = res.next;
            }
        })
    }
});