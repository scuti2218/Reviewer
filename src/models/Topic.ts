export interface ITopicProperties {
  title: string;
  description: string;
  version: string;
  token: string;
  code?: string;
  image?: string;
}

export default class Topic implements ITopicProperties {
  title: string;
  description: string;
  version: string;
  token: string;
  code?: string;
  image?: string;

  constructor(data: ITopicProperties) {
    this.title = data.title;
    this.description = data.description;
    this.version = data.version;
    this.token = data.token;
    this.code = data.code;
    this.image = data.image;
  }
}
