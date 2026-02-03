---
layout: post
title: "REST APIs – .NET Core Web API 2 versus SailsJS versus Express / TypeORM"
date: 2020-10-12 12:29:26 +0000
author: "Abi"
featured_image: "https://static.wixstatic.com/media/5fdde1_ae9747f97e0a48ba961a888a3e345974~mv2.jpeg/v1/fit/w_700,h_368,al_c,q_80/file.png"
excerpt: "Building a REST API driven application? You are certainly spoilt for choices with the numerous frameworks in all kinds of tech stacks..."
---

Building a REST API driven application? You are certainly spoilt for choices with the numerous frameworks in all kinds of tech stacks that have hit the market off late. While we cannot practically be covering the pros and cons of all, we do have three frameworks that standout in the Open Source world – .NET Core Web API 2 which comes from the Microsoft shop, SailsJS which internally leverages Express and Waterline ORM and an Express + TypeORM combination. Each three have very distinctive advantages and drawbacks that we will look at. Before we start, I do have a confession. Loopback has intentionally been left out of this discourse. Well, I have bit of a history with that framework. Not that I hate it, but back in 2015, I went from choosing it to build a complex enterprise grade API backend in Loopback to phone calls with IBM sales staff explaining me why paying several thousands of dollars was the way to go for us. Ever since I hung up on the sales people at IBM, I have never looped back to Loopback (pun intended), and discovered far more interesting projects instead. However things have changed dramatically with the release of Loopback 4, and it deserves to be covered in a completely separate write up.

## [SailsJS](https://www.sailsjs.com/) (NodeJS + Express + Waterline ORM)

SailsJS beats every other framework hands down when it comes to the time it takes to get your first API setup up and running. There are very good reasons for it to have achieved that title. I have architected several solutions with a SailsJS backend – a high grade security chat app, a social networking website for pet owners, a job portal and a food ordering system to name a few.

### Pros

- **End to end API ecosystem** – When you start with SailsJS, the only additional dependency you need to address is the connector to the Database, and nothing else practically is required to be configured (at least not right away). But even that is optional, you could start with API development even before having finalized your Database system. Let the argument between NoSQL vs RDBMS rage on while your team can actually start building the API on the side. Sails comes packaged with sails-disk which stores/retrieves the data from local disk or in memory. Being based off of Express means it supports policies, familiar req res objects, controllers and models almost the same way that Express does
- **Blueprints API** – When you can start making GET, PUT, POST, DELETE calls almost immediately – life really doesn’t get better than this. Imagine running these short few commands to get your first API up and running:

Off you go! Now point your Postman to localhost:1337/items and you can do your first POST (post any JSON, it will get stored onto sails-disk), GET PUT DELETE etc.

- **Express under the hood**– In the Node world, Express is the gold standard for REST API development and that’s what is kicking stuff under the hood in Sails. The good part is, if you are familiar with Express, you already know how to work with 50% of SailsJS
- **Connectors** – You have connectors for every major Database system – RDBMS as well as NoSQL.
- **Waterline ORM** – While Waterline isn’t the best ORM in the world, it gets the basic job done and pretty quickly. It lacks advanced features specifically in respect to NoSQL database systems which make it a challenge to work with for more advanced tasks. For example, you cannot query nested JSON objects with as much ease or simplicity as the native query language provides.
- **Sails Sockets** – Web sockets are first class citizens with Sails. You can listen to changes on any model you may have created from the get go without having to write any additional code

### Cons

There are several. Read on.

- **Waterline ORM** – The underlying Waterline ORM can be a terrific boost when you are building a quick API backend for a relatively simple app. The moment you get into advanced queries, cracks start showing up. The biggest advantage that any ORM provides is database vendor independence. Yes, Waterline gets you that, but not efficiently. Inevitably, you would have to fall back onto native queries and that’s when you loose vendor independence
- **TypeScript Support** – While it will be incorrect to say that TypeScript support is missing, it is by no means a first class citizen in the Sails world. You can still write your Models and Controllers in TypeScript, but that is the end of it. The SailsJS framework itself still relies on the loosely typed underlying Javascript objects. Those who understand the perils of loosely typed backend programming are going to be immediately turned off by this, and understandably so
- **Production Deployment** – OK most problems related to production deployment are shared across NodeJS based Frameworks including Express. When you want to take your API to a serious production environment, several key challenges creep in. For instance, there is no standard simple way of configuring high grade web servers like Apache or IIS to work well with SailsJS or Express apps. The steps are convoluted and unorganized. E.g. You would like to use pm2 to manage your NodeJS process. But how do you get pm2 to work efficiently with Apache or IIS? Go figure.

## .NET Core Web API 2

Microsoft under Satya Nadella has got somethings done right in a phenomenal way. The first was to embrace Open Source rather than compete with it. As a result, we got .NET Core and a bunch of application building capabilities that came along with it. We can now build and deploy .NET command line apps, ASP.NET MVC web apps and RESTful APIs with Web API 2 using .NET Core and remain fully in the realm of cross-platform open source code base. Having said that, why would we discuss a .NET based framework amongst Node based frameworks? Because in my opinion, these frameworks are the fastest way to build RESTful APIs across the technology landscape (note just in Node and .NET world) and I would love to be challenged on that thought. Back to Web API 2

### Pros

- **C#**– Strongly typed, highly object oriented, mature and beautiful. Very few languages can pride themselves on these qualities and be backed by hundreds of thousands of programmers. For the folks who are saying in their heads, “Ok smarty, tell me one language feature that gets me to move my butt onto the C# side”, for them I have one word answer – LINQ
- **.NET Core** – Open Source, cross-platform and fast, .NET Core negates all the dis-qualities that were associated with the traditional .NET Framework. Plus the benefit of having a large programmer base addressing these technologies is a BIG plus in tackling the learning curve
- **Entity Framework Core** – Those who have worked with EntityFramework 6 or earlier, know the power of this now-mature ORM framework. Without going too much into the nuts and bolts of the framework itself, let me say this in a nutshell – Waterline x Nitro boosters = EntityFramework. EFCore is fast, efficient, powerful and highly configurable.
- **Rapid API Development** – While beating Sails in speed of getting started is quite a challenge for most frameworks, .NET Core Web API 2 isn’t too far behind, thanks to EFCore. You can create migrations for your Models to the database or scaffold models based on your database schema relatively easily. In most cases it is only a few short commands
- **Visual Studio Code, Azure, IIS and more** – This is one of the major strengths of building with .NET Core. You feel right at home with other Microsoft offerings. Develop on VS Code, deploy on Azure all in just minutes! Interestingly, Visual Studio Code does not come prepackaged with C# support. You need to add a plugin, but once that’s done, its easy as pie. You can build, debug and deploy apps from right within Visual Studio Code and work on your favorite Linux Distro while at it or on a Mac (Ok you get the point – for me nothing is more important than being cross-platform not only for deployment, but also during development)
- **Compatible with Enterprise Systems** – When building for Enterprises, you will encounter challenges you never would while developing for smaller projects. Take an example of Integrated Security with SQL Server. I am building an API and I cannot store plain text passwords in connection string configurations. The only way I can connect to a SQL Server system is by using Integrated Security. I have gone through this painful exercise with an Express API and let me tell you, it was not pretty. We tried convincing the IT Security department of why it was just fine to store credentials in environment variables but all of that didn’t fly. We eventually found a workaround but the lack of Integrated Security support with most Node based SQL Server connector frameworks was a harsh reality we faced much, much further down the line during deployment.

### Cons

- **Not Enough Connectors**– Entity Framework Core does not support every database system and its brother. You have to research carefully before you make this jump. Here is a list of whats supported so far. If you are certain that the database vendor will not change in future and what you have now is supported by EFCore, go for it. You could still code for unsupported databases using direct queries but that would take you away from EFCore and the benefits it brings. It would then be equivalent to writing an API in Express (instead of Sails)
- **No TypeScript Support** – Full stack engineers are the future. And they love their language of programming to be the same across the front and back. While you can achieve that with something like Angular, TypeORM and Express, you cannot claim that with .NET Core Web API 2, at least for now. The reason I say that, is because conceptually .NET Core is language independent and may support compilation of TypeScript into Intermediate Language (IL). But till that happens, you will end up coding in different front end and backend languages
- **Microsoft**– Those who have been in the industry long enough, know the perils of locking yourself in with Microsoft. As I started by saying that Microsoft has changed significantly since their new CEO, anything coming out of Redmond has to be taken with precaution

## TypeORM and Express

If the title leads you on to it, you would have guessed this is not an API framework like SailsJS. It is a combination of two frameworks to achieve the same/similar result though. TypeORM is exclusively an ORM framework. Express on the other hand, is exclusively an API framework and has no built in ORM or even database connection for that matter. The beauty is, both these frameworks focus on their strengths while playing well with each other, just like Web API 2 + EFCore.

### Pros

- **TypeScript** – Finally! We can say that our programming language would remain the same in the front and the back end. This is a major advantage for those aiming to build cross-functional teams working on Angular or React web apps
- **Excellent ORM features** – What bogged down SailsJS was Waterline but in case of TypeORM, being a truly world class ORM is what the focus is. One look at TypeORM’s documentation will have you convinced that it should be able to handle most of your complex ORM needs. It still lacks the beauty of LINQ with EFCore, but it gets the job done really well! Has the most powerful Query Builder in the NodeJS world, IMHO
- **Support for Indices** – Well this is important provided you are looking at database vendor independence. Telling the ORM which column has indices is a neat way to ensure whenever you migrate to a different provider, the indices go along. Plus it is great for Continuous Integrations because your test database can be rebuilt with indices
- **Listners, Migrations, Query Builder and more** – I will stop short of explaining each of these, but do read about these features. These make TypeORM stand out and a much better candidate for an Enterprise grade use case
- **Well Documented**– The official website should answer most of your questions. It is a well documented framework
- **Connectors**– Has a wide selection of database connectors. The current connectors support includes MySQL / MariaDB / Postgres / CockroachDB / SQLite / Microsoft SQL Server / Oracle / sql.js / MongoDB

### Cons

- **Poor “Getting Started” experience** – The setup is nothing as simple as SailsJS or Web API + EFCore. You are on your own to define the project structure and code layout. In short, you either start with a boilerplate or create your own structure from scratch. There are decent boilerplates to start with but you have to look out for how upto-date they are. You will need to setup a project with TypeORM, Express and any other dependencies you anticipate
- **Not an end-to-end API ecosystem** – Unlike Web API 2 + EF Core, these two frameworks don’t recognize each other out of the box. They rely on your boilerplate or your project setup to get anywhere close to a “point-and-shoot by Postman” scenario

## Conclusion

Toeing the line of every conclusion written for a comparison based article ever written, it all comes down to a few of these things -

- Your teams' and your preference
- The requirements of your project
- Technology choice of your organization
- The ability of your framework to stack up to future requirements

If you want my personal conclusion, it is even more simpler -

- Building an API from scratch for a relatively small app which needs fast turnaround time? Go with SailsJS - without a doubt, this is the fastest way to build self hosted API service
- Building a large scale API for an Enterprise grade system that will require communication with possible legacy systems or will primarily be deployed in the realm of Redmond based products? Go with .NET Core Web API 2 + EntityFramework Core
- You have the time to build out the best API backend provided it looks towards the future of cross-functional programming teams? This one splits out further more -
- Is your front end built on Javascript? e.g. Angular 1.x - Go with SailsJS
- Is your front end built on C# or .NET? e.g. ASP.NET MVC or Xamarin App? Web API 2 it is...
- Is your front end built on TypeScript? e.g. Angular 2+, React etc.? Go with TypeORM and Express

There are several more choices that we will ostensibly be spoilt to choose from. Take them for a spin and do your thing, figure out what's best for you, your team and the future of your product.

Originally posted on:

[https://www.linkedin.com/pulse/rest-apis-net-core-web-api-2-versus-sailsjs-express-chatterjee/](https://www.linkedin.com/pulse/rest-apis-net-core-web-api-2-versus-sailsjs-express-chatterjee/)

[http://www.abhishekchatterjee.com/?p=158](http://www.abhishekchatterjee.com/?p=158)
