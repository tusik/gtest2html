class TagManager {
  constructor() {
    this.availableTags = new Set([]);
    this.tagElementsMap = {};
    this.tagContainers = {};
    this.tagElementsMap['none'] = [];
    this.badgeElements = {};

    this.enabledTags = new Set([]);

    this.tagContainerTagsMap = {};

    this.initialize();
    this.insertTagBades();
  }

  initialize() {
    var self = this;
    $('.single-testsuite-container').each(function(){
      var parentContainer = $(this);
      var parentContainerId = parentContainer.attr('id');
      self.tagContainers[parentContainerId] = parentContainer;
      self.tagContainerTagsMap[parentContainerId] = new Set([]);

      parentContainer.find('tr[data-tags], th[data-tags]').each(function(){
        var tagElement = $(this);
        var tagsAttr = tagElement.attr("data-tags");

        // Get available tags.
        var tagItem = {};
        tagItem.tagElement = tagElement;
        tagItem.parentId = parentContainerId;
        tagItem.enabledTags = [];

        if (tagsAttr != '') {
          var tagsArray = tagsAttr.split(';');
          for(let tag of tagsArray) {
            self.availableTags.add(tag);
            self.tagContainerTagsMap[parentContainerId].add(tag);

            if(self.tagElementsMap[tag] == null) {
              self.tagElementsMap[tag] = [];
            }
            self.tagElementsMap[tag].push(tagItem);

            // Add badges to the tag element.
            var badgeElement = $(document.createElement("span"));
            badgeElement.addClass("badge badge-pill badge-light");
            badgeElement.attr('style', 'margin-left: 5px;');
            badgeElement.append(tag);
            tagElement.find('.testcase-badges').append(badgeElement);
          }
        } else {
          self.tagElementsMap['none'].push(tagItem);
        }
      });
    });
  }

  insertTagBades() {
    var self = this;
    $('.tags-container').each(function() {
      for(let tag of self.availableTags.values()) {
        var button = $(document.createElement("button"));
        button.addClass("btn btn-sm btn-secondary tag-button");
        button.attr("tag", tag);
        button.text(tag + " ");

        var badgeItem = $(document.createElement("span"));
        badgeItem.addClass("badge badge-pill badge-light");
        badgeItem.text(self.tagElementsMap[tag].length / 2);

        button.append(badgeItem);

        var badgeElement = {};
        badgeElement.element = button;
        badgeElement.isClicked = false;
        self.badgeElements[tag] = badgeElement;

        $(this).append(button);
      }
    });
  }

  onClick(tag) {
    var self = this;

    // Update badge element.
    var badgeElement = self.badgeElements[tag];
    badgeElement.isClicked = !badgeElement.isClicked;

    if( badgeElement.isClicked) {
      self.enabledTags.add(tag);
      badgeElement.element.removeClass("btn-secondary").addClass("btn-success");
    } else {
      self.enabledTags.delete(tag);
      badgeElement.element.removeClass("btn-success").addClass("btn-secondary");
    }

    var tagElementsArray = self.tagElementsMap[tag]
    for(var tagElementIdx in tagElementsArray) {
      var tagElement = tagElementsArray[tagElementIdx];

      if(badgeElement.isClicked) {
        tagElement.enabledTags.push(tag);
      } else {
        var index = tagElement.enabledTags.indexOf(tag);
        if(index != -1) {
          tagElement.enabledTags.splice(index, 1);
        }
      }
    }

    self.updateView();
  }

  updateView() {
    var self = this;

    // Update badges classes.
    if(self.enabledTags.size == 0) {
      $('#total-test-summary').show();
      $('.single-test-summary').show();
    } else {
      $('#total-test-summary').hide();
      $('.single-test-summary').hide();
    }

    var containerEnabledTagItemsCount = {};
    for(var tag in self.tagElementsMap) {
      var tagElementsArray = self.tagElementsMap[tag];
      for(var tagElementIdx in tagElementsArray) {
        var tagItem = tagElementsArray[tagElementIdx];

        if(containerEnabledTagItemsCount[tagItem.parentId] == null) {
          containerEnabledTagItemsCount[tagItem.parentId] = 0;
        }

        if(tagItem.enabledTags.length > 0 || self.enabledTags.size == 0) {
          tagItem.tagElement.show();
          containerEnabledTagItemsCount[tagItem.parentId]++;
        } else  {
          tagItem.tagElement.hide();
        }
      }
    }

    for(var containerId in self.tagContainers) {
      if(containerEnabledTagItemsCount[containerId] == null ||
        containerEnabledTagItemsCount[containerId] == 0) {
        self.tagContainers[containerId].hide();
      } else {
        self.tagContainers[containerId].show();
      }
    }

    for(var tagContainerId in self.tagContainerTagsMap) {
      var containingTags = Array.from(self.tagContainerTagsMap[tagContainerId]);
      var filteredTags = containingTags.filter(element => self.enabledTags.has(element));

      var navElements = $('.nav a[href="#' + tagContainerId + '"]')
      console.log(self.enabledTags);
      if(filteredTags.length == 0 && self.enabledTags.size > 0) {
        navElements.hide();
      } else {
        navElements.show();
      }
    }
  }
};

$(document).ready(function() {
  // Initialize the stacktable for responsive tables.
  $('.testcase-table').stacktable({myClass: 'testcase-stackable', headIndex: 1});

  // Make the height of the testcase-sidebar-list fix, so that removing and adding items by clicking
  // the tag badges not influences the height.
  var testcaseSidebarList = $('#testcase-sidebar-list');
  testcaseSidebarList.attr('style', 'height: ' + testcaseSidebarList.height() + 'px;');
  // Add the data tags to the stacktable.
  $('.single-testsuite-container').each(function() {
    var container = $(this);
    var untaggedElements = container.find('.stacktable.small-only .st-head-row:not(.st-head-row-main)');

    var idx = 0;
    var taggedElements = container.find('.testcase-table.large-only tr.testcase-row').each(function(){
      $(untaggedElements[idx]).attr('data-tags', $(this).attr('data-tags'));
      idx++;
    });
  });

  // Overwrite the default on-page link behaviour for nav-links to fix the scrolling behaviour.
  $(".nav-link").click(function(e) {
      e.preventDefault();
      var href = e.target.href, id = "#" + href.substring(href.indexOf("#") + 1);
      $(window).scrollTop($(id).offset().top - 76);
  });

  var tagManager = new TagManager();

  $('.tag-button').click(function(event){
    event.preventDefault();
    var badgeElement = $(this).find(".badge").one();
    var tag = $(this).attr("tag");
    tagManager.onClick(tag);
  });
});
