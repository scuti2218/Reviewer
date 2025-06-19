<template>
  <section id="fr_fragmentTableTopics" class="main-container">
    <h1 id="fr_fragmentTableTopics-title">TOPICS</h1>
    <section id="fr_fragmentTableTopics-contents">
      <section
        class="fr_fragmentTableTopics-topic outline-black"
        v-for="topic in state.favorites"
        @mouseenter="cmdMouseEnter(topic.title)"
        @mouseleave="cmdMouseLeave"
      >
        <section id="fr_fragmentTableTopics-topic-details">
          <section
            id="fr_fragmentTableTopics-topic-left"
            class="fr_fragmentTableTopics-topic-content"
          >
            <h5>{{ topic.title }}</h5>
            <h6>{{ topic?.code }}</h6>
          </section>
          <section
            id="fr_fragmentTableTopics-topic-right"
            class="fr_fragmentTableTopics-topic-content"
          >
            <h5>{{ topic.title }}</h5>
            <h6>{{ topic?.code }}</h6>
          </section>
        </section>
        <section id="fr_fragmentTableTopics-topic-buttons">
          <div :class="['button-sample', { show: canShow(topic.title) }]">
            <StarIcon />
          </div>
          <div :class="['button-sample', { show: canShow(topic.title) }]">
            <GreaterThanIcon />
          </div>
        </section>
      </section>
    </section>
  </section>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { ITopicProperties } from "@/models";
import { StarIcon, GreaterThanIcon } from "@/components";

const defaultState = {
  favorites: [
    {
      title: "Title 1",
      description: "this is a blank",
      version: "0.1.1",
      token: "123456",
      code: "12345",
    },
    {
      title: "Title 2",
      description: "this is a blank",
      version: "0.1.2",
      token: "123456",
      code: "289465",
    },
    {
      title: "Title 3",
      description: "this is a blank",
      version: "0.1.2",
      token: "123456",
    },
  ] as ITopicProperties[],
  hoveredTopic: "" as string,
};
const state = reactive(defaultState);

const cmdMouseEnter = (title: string) => (state.hoveredTopic = title);
const cmdMouseLeave = () => (state.hoveredTopic = "");
const canShow = (title: string) => state.hoveredTopic === title;
</script>

<style scoped>
#fr_fragmentTableTopics {
  width: 100%;
  background-color: var(--bs-primary);
}

#fr_fragmentTableTopics-title {
  align-self: flex-start;
}

#fr_fragmentTableTopics-contents {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.fr_fragmentTableTopics-topic {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  border-radius: 10px;
  gap: 20px;
  background-color: var(--bs-light);

  &:hover {
    background-color: var(--bs-light-darken);
  }
}

#fr_fragmentTableTopics-topic-details {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  padding-left: 20px;
}

.fr_fragmentTableTopics-topic-content {
  min-height: 100%;
  min-width: 30px;
}

#fr_fragmentTableTopics-topic-buttons {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
}

.button-sample {
  height: 60px;
  min-width: 0px;
  max-width: 0px;
  transition: all 100ms ease-in;
  overflow: hidden;

  &.show {
    min-width: 60px;
    max-width: 60px;
  }

  &:hover {
    background-color: var(--bs-primary-lighten);
  }
}
</style>
