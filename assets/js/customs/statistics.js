// Category statistics - using pre-calculated stats for fast sidebar loading

// Helper function to get count from category-stats
function getCategoryCount(stats, categoryPath) {
  return stats[categoryPath] || 0;
}

$(function () {
  // Load lightweight category stats for sidebar
  $.ajax({
    url: location.origin + "/data/category-stats.json",
    dataType: "json",
    success: function (categoryStats) {
      // Sidebar Num of Posts - Main Menu
      $(".nav__sub-title-name > a").each(function (idx, item) {
        var $item = $(item);
        var itemCat = $item.attr("id").split("sidebar-")[1];
        var numTot = getCategoryCount(categoryStats, itemCat);
        $item.append('<span class="nav__sub-title-stat">' + numTot + "</span>");
      });

      // Sidebar Num of Posts - Sub Menu
      $(".nav__item-children > li > a").each(function (idx, item) {
        var $item = $(item);
        var itemCats = $item.attr("id").split("sidebar-")[1];
        var numTot = getCategoryCount(categoryStats, itemCats);
        $item.append('<span class="nav__item-children-stat">' + numTot + "</span>");
      });

      // Sidebar Afterprocess - Resize sidebar font
      resizeSidebarFont();

      // Whole TOC Page
      var memoType = $(".memo").data("type");
      if (memoType == "toc") {
        $(".wholetoc__category-title > a").each(function (idx, item) {
          var $item = $(item);
          var itemCats = $item.attr("href");
          if (itemCats.substr(0, 1) == "/")
            itemCats = itemCats.substring(1, itemCats.length);
          if (itemCats.substr(itemCats.length - 1, 1) == "/")
            itemCats = itemCats.substring(0, itemCats.length - 1);
          itemCats = itemCats.split("/").join("|");
          var numTot = getCategoryCount(categoryStats, itemCats);
          $item.append('<span class="wholetoc__category-stat">(' + numTot + ")</span>");
        });
      }
    },
    statusCode: {
      404: function () {}
    }
  });

  // Post Pagination - load full posts data only when needed
  let $pagination = $(".post-pagination");
  if ($pagination.length > 0) {
    $.ajax({
      url: location.origin + "/data/posts-info.json",
      dataType: "json",
      success: function (data) {
        var postsGroupByCats = {};

        function groupByCategories(post, group, nestedIdx) {
          nestedIdx = nestedIdx || 0;
          var postKey = post.categories[nestedIdx];
          group[postKey] = group[postKey] || { posts: [], children: {} };
          if (nestedIdx >= post.categories.length - 1) {
            group[postKey]["posts"] = group[postKey]["posts"] || [];
            group[postKey]["posts"].push(post);
          } else {
            group[postKey].children = groupByCategories(post, group[postKey].children, nestedIdx + 1);
          }
          return group;
        }

        function getPostsFromGroup(group, categories, idx) {
          idx = idx || 0;
          var catKey = categories[idx];
          if (!group[catKey]) return [];
          if (idx < categories.length - 1) {
            return getPostsFromGroup(group[catKey].children, categories, idx + 1);
          }
          return group[catKey].posts || [];
        }

        $(data).each(function (idx, item) {
          postsGroupByCats = groupByCategories(item, postsGroupByCats);
        });

        var postsInCurCats = getPostsFromGroup(
          postsGroupByCats,
          $pagination.data("categories").split("/")
        );

        if (postsInCurCats.length > 1) {
          $pagination.removeClass("hidden");

          sortArrayOfObjectsByKey(postsInCurCats, "date", "asc");
          sortArrayOfObjectsByKey(postsInCurCats, "post-order", "asc");

          var curPath = window.location.pathname;
          var curPathIdx = postsInCurCats.findIndex(function (item) {
            return item.url == curPath;
          });

          if (curPathIdx > -1) {
            var prevPost = postsInCurCats[curPathIdx - 1];
            if (prevPost) {
              $(".pagination__pager.pager-prev").attr("href", prevPost.url + "#page-title");
              $(".pagination__pager.pager-prev .pager-title").text(
                $("<textarea />").html(prevPost.title).text()
              );
            } else {
              $(".pagination__pager.pager-prev").css("display", "none");
            }

            var nextPost = postsInCurCats[curPathIdx + 1];
            if (nextPost) {
              $(".pagination__pager.pager-next").attr("href", nextPost.url + "#page-title");
              $(".pagination__pager.pager-next .pager-title").text(
                $("<textarea />").html(nextPost.title).text()
              );
            } else {
              $(".pagination__pager.pager-next").css("display", "none");
            }
          }
        }
      },
      statusCode: {
        404: function () {}
      }
    });
  }
});
