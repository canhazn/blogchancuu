<template>
  <div class="container">
    <nav class="navbar">
      <a
        class="navbar-brand text-white font-italic font-weight-bolder"
        href="{% url 'home' %}"
      >BLOGCHANCUU</a>
      <ul class="navbar-nav">
        <li class="nav-item" id="search-btn" style="cursor: pointer;">
          <div class="d-flex justify-content-center align-items-center">
            <span class="material-icons">search</span>
          </div>
        </li>
      </ul>
      <div class="input-group form-inline search-input">
        <input type="text" id="search" class="form-control" placeholder="Search" />
      </div>
    </nav>
  </div>
</template>

<script>
module.exports = {
  delimiters: ["[[", "]]"],
  data: function() {
    return {
      greeting: "Hello"
    };
  },
  mounted: function() {

    // show od hide search
    $("#search-btn").click(function() {
      $(".search-input").toggleClass("active").focus;
      $(this).toggleClass("animate");
    });    

    // scrope function search post
    (function() {
      var timeout = {};
      var update = function() {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
          var key = $("#search").val();
          store.dispatch("filterPost", { search: key });
        }, 1000);
      };

      $("input#search").keyup(update);
      $("input#search").change(update);
    })();

    
  }
};
</script>