Introduction
I created a Cash Book app using only simple prompts, that is, "No Programming Code".
The following videos show how it was done.
[YouTube: Generative AI + dFrame(PaaS) make your Business App with no code (Shortened version: 3min)](https://www.youtube.com/watch?v=0Z7qzh3-ShE)

[YouTube: Generation AI (Chat2DB) + "dFrame" (Open Source) Build up Web APP without programing](https://www.youtube.com/watch?v=DeZ9StKZ6XU)

This involves sending the three prompts listed in the appendix to Generative AI Chat2DB, and then performing the following operations on the PaaS dFrame.
Those are:
①  To create a link to the Cash Book table that Chat2DB outputs to.
②  To register the procedure maintaining "Balance" , that Chat2DB created, as "triggered" process for Cash BookTable
③  To register the procedure generating PDF List, that Chat2DB created, as data source for "report schema" 
That's all !
This article introduces the design philosophy that made this possible and the open-source platform dFrame that implements it.

Why is New AI-Driven Development Scheme needed?

Because it offers a powerful antithesis (solution) to the recent problems of AI generating massive amounts of code, leading to a collapse of source code management (the "spaghetti code" problem).
Indeed, the source of the article "AI coding assistants increase developer output, but not company productivity"
, https://www.faros.ai/blog/ai-software-engineering, points out the following:
Drawing on telemetry from over 10,000 developers across 1,255 teams, Faros' recent landmark research report confirms:
• Developers using AI are writing more code and completing more tasks
• Developers using AI are parallelizing more workstreams
• AI-augmented code is getting bigger and buggier, and shifting the bottleneck to review
• Any correlation between AI adoption and key performance metrics evaporates at the company level

In fact, it's intuitively clear that while AI-driven development (AIDD) dramatically increases development speed, it faces four major challenges: hallucination (misgeneration), plaqueboxing/spaghetti code problem.

New AI-Driven Development Scheme 

It is clear that the key to solving those challenges lies in two things:
• Increasing the "granularity" of prompts to the generative AI
• Minimizing, or eliminating, the context for the generative AI

The following scheme provide the key to solving these two problems:
• MVC Model: The application's structural design should not be left to AI. That is, the structure of Model (business rules), Visual (UI), and Control (internal control) is assumed to be given.

• Chat2DB: Automatically generates SQL statements that constitute the "M (Model)" of the MVC model. Prompts are spent on generating information for the database structure and set operations.

• dFrame: An MVC model implementation PaaS. A no-code Agile tool.

MVC Model
The MVC model is a system implementation model. When implementing based on this model, the target of AI-driven development is divided into three functions: {"M" (model), "V" (view), and "C" (control)}.

Therefore, in AI-driven development using this scheme, the three-part division of {"M", "V", and "C"} improves the "granularity" of the generated targets, and allows for the selection of the most suitable AI model.

Furthermore,
▶"C" (Control): By generalizing use cases such as business applications and normalizing the interfaces between "M" and "V", "C" can be established and integrated as a platform and infrastructure.

▶"V" (view): By using languages ​​that dynamically generate HTML, such as Python/WTF, for generalization, the granularity of prompts for generating the UI improves. Furthermore, standard screen patterns can be applied.
▶ "M" (Model): A model consists of "objects" (schema + data) and "classes" (processes), but can be embedded in the database by satisfying the following conditions:
① Build "meta-information" for objects within the DB and make it accessible from "C" and "V"
② Include references and dependencies between objects and class activation trigger information in the meta-information
In other words, the generation requirements for individual objects and individual classes are defined as prompts and managed individually, increasing granularity. The generated code is stored in the database.

In this way, advancing AI-driven development under the MVC model scheme offers significant advantages. You can build apps by generating SQL statements in a "humble" way using natural language.

PaaS dFrame + Chat2DB

dFrame is a platform for developing applications using the MVC model and agile cycles.
dFrame is open source and can be downloaded from GitHub and used as is. You are also free to modify and improve it.

dFrame itself uses the MVC model as its design pattern. In fact, the design components and the "metadata normalization" functionality for the UI of dFrame are implemented (recursively) within a MySQL database.
In the implementation phase of application development, simply generating schemas, procedures, and test data for the "M" (Model) in Chat2DB allows you to immediately run tests on the list display screen.

Furthermore, as the cycle progresses to the implementation cycle for improving UI usability, you can also create unique HTML files under Python Flask/WTF. For PDF report creation, you proceed to define the stored procedure that generates the report data.
