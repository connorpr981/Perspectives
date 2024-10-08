**Dwarkesh Patel** _00:00:00_

Today, I'm chatting with [Patrick McKenzie](https://www.kalzumeus.com/). He is known for many things on the Internet. He's known as [patio11](https://x.com/patio11). Most recently he ran [VaccinateCA](https://worksinprogress.co/issue/the-story-of-vaccinateca/), which probably saved a high four-figure number of lives during COVID. He also writes an excellent newsletter called _[Bits about Money](https://www.bitsaboutmoney.com/)_.

Patrick, welcome to the podcast.

**Patrick McKenzie** _00:00:18_

Thanks very much for having me.

**Dwarkesh Patel** _00:00:19_

VaccinateCA has a lot of important lessons about what parts of our institutions are fucked up. Before we get into what's fucked up, what was VaccinateCA?

**Patrick McKenzie** _00:00:30_

In early 2021, we were quite concerned that people were making 20, 40, 60 phone calls to try to find a pharmacy that actually had a dose of the [COVID vaccine](https://en.wikipedia.org/wiki/COVID-19_vaccine#) in stock and could successfully deliver it to them.

I [tweeted](https://x.com/patio11/status/1349577791537250310) out randomly that it was insane. Every person or every caregiver is attempting to contact every medical provider in the state of California to find doses of the vaccine. California clearly has at least one person capable of building a website where you can centralize that information and send everybody to the website. I said, “if you build that website, I’ll pay for the server bill or whatever.”

[Karl Yang](https://karlyang.net/) took up the gauntlet and invited 10 of his best friends and basically said “all right, get in, guys. We're going to open source the availability of the vaccine in California by tomorrow morning.” This is at like 10:00 p.m. at night, California time. I lurked down into the Discord and gave a few pointers on making scaled calling operations. One thing led to another and I ended up becoming the CEO of this initiative.

At the start, it was just this hackathon project of a bunch of random tech people who thought, “hey, we can build a website, make some phone calls, maybe help some people find the vaccine at the margin.”

It grew a little bit from there. We essentially ended up becoming the public-private partnership that was the clearinghouse for vaccine location information for the United States of America. That felt a little weird at the time and continues to.

**Dwarkesh Patel** _00:01:48_

Here’s the obvious question. Why was this something that people randomly picked up on a discord server?

Why wasn't this an initiative by an entity delegated by the government? Why didn’t the White House or the pharmacies have a website where you can just sign up for an appointment?

**Patrick McKenzie** _00:02:07_

There are so many reasons and a whole lot of finger-pointing going on.

One of the issues was that almost no actors in the system said, "yes, this is definitely my responsibility." Various parts of our nation's institutions — county-level public health departments, governors' offices, and two presidencies — all said, "I have a narrow part to play in this, but someone else has to do the hard work of actually putting shots in people's arms. Clearly someone else is dealing with the logistics problem, right?"

The ball was dropped comprehensively. No one at the time really had a plan for picking it up. No one felt it was incentive-compatible for them specifically to pick it up right now. “It would have been great if someone could do this, but just not me.”

**Dwarkesh Patel** _00:02:54_

The context was that it was very important that people get vaccines at the time. These delays mattered. You can account for it in the number of lives saved. You can even look at how much the stock market moved when vaccine news was announced.

It was clear it was worth trillions of dollars to the economy that the vaccine be delivered on time. It should have been priority #1 that people know where the vaccine is. It raises a meta question. Why did I hear about this problem for the first time when I read your [article](https://worksinprogress.co/issue/the-story-of-vaccinateca/)?

There's been a lot of controversy after COVID about people pointing fingers about masks or different protocols. Why was this not a bigger issue? Why were people not getting called in front of Congress about our inability to deliver the one thing needed to arrest the pandemic as fast as possible?

**Patrick McKenzie** _00:03:47_

I wrote 27,000 words on this in my article in _Works in Progress_ called ["The Story of VaccinateCA”](https://worksinprogress.co/issue/the-story-of-vaccinateca/) which goes into some of the nitty-gritty. Broadly, it's a matter of incentives more than people choosing to do evil things. Although we did choose to do evil things  and we can probe on that if you want to.

When [Obamacare](https://en.wikipedia.org/wiki/Affordable_Care_Act) was first debuting, the federal government institutionally learned one wrong lesson from the [Healthcare.gov rollout](https://en.wikipedia.org/wiki/HealthCare.gov#Issues_during_launch), which would have terrible consequences. Many actors in the federal government and political parties came away thinking that a president can doom the legacy of their signature initiative if "those bleeping tech folks don't get their bleeping act together."

As a result, the United States has decided that virtually nothing — up to and including the potential of national annihilation — will cause us to actually put our chips behind solving a software problem. That's somebody else's problem, someone who doesn't have to deal with an electoral mandate or getting called in front of Congress. It’s somebody else’s problem.

Unfortunately, software is eating the world. Delivering competence in the modern world requires being competent at software. The United States will tell you differently. There are wonderful people in the government attempting to change this. However, broadly speaking on an institutional level, the United States federal government has abdicated software as a core responsibility of the government.

**Dwarkesh Patel** _00:05:15_

I understand why they didn't initially want to pursue this project. I still don't understand why after everything went down, it isn’t more of a news item that this was a problem that was not solved?

**Patrick McKenzie** _00:05:29_

We're [memory-holing](https://en.wikipedia.org/wiki/Memory_hole) a lot of things that happened in the pandemic. I wish we wouldn't. It’s partly because of political incentives and because we're approaching an election year. It’s also because of the quirky way that American parties and candidates bounce off each other.

It's in no one's real incentive to say, "okay, I would like to relitigate the mask issue for a moment." [We told people that masks don't block airborne viruses](https://www.usatoday.com/story/news/health/2020/02/17/nih-disease-official-anthony-fauci-risk-of-coronavirus-in-u-s-is-minuscule-skip-mask-and-wash-hands/4787209002/). We were quite confident of that. The entire news media backed us up on it. Then we 180’d a month later. No one wants to relitigate that.

No one wants to relitigate that California imposed [redlining](https://en.wikipedia.org/wiki/Redlining) in the provision of medical care. That was wrong and evil. However, the party that was pro-redlining does not normally like saying that it is pro-redlining. The other party does not really consider that a hugely salient issue.

There are no debates and no one is asking [Governor Newsom](https://en.wikipedia.org/wiki/Gavin_Newsom), "you got on TV and said that you were doing geofencing for the provision of medical care. Geofencing in that context was the same as redlining. Can you explain your support for redlining?" No one has asked Newsom that question. Maybe someone should. We're surrounded by the effects of incentives and the effects of iterated games. Sometimes they don't play out the way we would ideally like them to play out.

**Dwarkesh Patel** _00:06:52_

I still don't feel like I really understand. Is it that everybody has blood on their hands? That’s still confusing.

If you lost a war, you don’t just brush it aside. The generals would have to come up in front of Congress and be like, "what happened? why didn't we get that battlefield?" Actually, we just lost a war. Maybe that didn't happen.

**Patrick McKenzie** _00:07:19_

If one goes over the history of military conflicts, I don't know how many losers on either side of the conflict ever actually did that reckoning of "hey, could we attempt to win in the future?"

There was a broad lack of seriousness across many trusted institutions in American society — in the government, in civil society, in the tech industry — about really approaching this like a problem we want to win. A wonderful thing about our country and our institutions is that on things that are truly important to us, we win outlandishly because we are a rich and powerful nation. Yet this was obviously a thing where we should have decided to win. We fundamentally did not approach it as a problem that we needed to win on.

**Dwarkesh Patel** _00:07:58_

Let’s go back to the object level here. Instead of different people calling different pharmacies and asking whether they have the vaccine, people who have not read your article would assume that either some company or the government would build a platform like this. You explained why the government didn't do it. The pharmacies might build a platform like this.

I want to meditate on the incentives that prevented random big tech companies or Walgreens from building this themselves. Can you explain that?

**Patrick McKenzie** _00:08:31_

With the federal government and the state government, the American governmental system is quite complex. There were multiple distinct supply chains, with multiple distinct technological systems, tracking where these vials were headed all over the country. There were many attempts at various levels of the government to say, "hey, can we commission a consultancy to build a magical IT solution that will get these databases to talk to each other?" Those largely failed for the usual reasons that government software procurement projects fail.

Why didn't tech build it? I'm constrained on what I can say and cannot say. I know a little more than this answer. I will give you part of the answer. The tech industry — both at the level of AppAmaGooFaSoft, which is my funny sardonic way to refer to some of the most powerful institutions in the world, and many other places that hire many smart engineers who can build the world's least impressive inventory tracking system — felt political pressure in the wake of the [January 6th events](https://en.wikipedia.org/wiki/January_6_United_States_Capitol_attack) in the United States.

This is another thing that's gone down the rabbit hole. In the immediate wake of the January 6th events, people in positions of authority very clearly tried to lay that at the feet of the tech companies. Internally, the tech companies have policy teams, the teams that are supposed to make the company legible to the government and avoid government yanking permission to do business. Those teams, their communications teams, PR departments, they told everyone in the company, "mission number one right now, do not get in the newspaper for any reason. We are putting our heads down."

A thing that might not be obvious to most people in the world is that AppAmaGooBookSoft literally have teams of people whose job is public health because they are the operating system of the world right now. The operating system of the world needs public health care. Those teams said, "hey, we've got this thing" and other people in the company might have overruled them and said, "it would be really bad right now to have the tech industry saying we're better at the government's job than the government is. So shut that down."

**Dwarkesh Patel** _00:10:38_

That's so insane.

**Patrick McKenzie** _00:10:41_

It absolutely is. The local incentives make sense in the meeting when you're saying it. You are not in that meeting projecting, "I'm going to cause tens of thousands of people to die at the margin by making this call." Yet that call was made.

**Dwarkesh Patel** _00:10:57_

There are two culpable actors here. You could say the first is the big tech companies for not taking the political risk. What is even more reprehensible is the fact that they probably correctly thought that appearing more competent than the government — and saving tens of thousands of lives as a result — would be held against them and significantly impact their other businesses.

Suppose that they had built the software. Let's play with the scenario. What would happen then? Would they get hauled in front of Congress and explain why they weren't delivered even faster because of the ultimate bottlenecks in the supply chain? What would happen if they built it and it's better than the government's?

**Patrick McKenzie** _00:11:43_

So many things could happen. This has sometimes been called the Copenhagen Principle of Culpability.

If you build the thing, various actors in our system will assume, "okay, now you're responsible not just for the consequences of the thing you built, but for the totality of consequences of everything associated with the American vaccination effort. You built the thing, you big tech geniuses, but what did you do about localization? You didn't do enough about localization. You hate \[name group of people here\], don't you? See the disparity in death rates between demographic A and demographic B? Why haven't you fixed that yet? You have killed so many people."

No one in government who is making that moral calculation says, "I have responsibility for killing people by doing nothing." The person who is doing anything has the responsibility for killing people by taking up the burden of doing something. It is an absolutely morally defensible thing, which you will see over and over again in our discourse.

**Dwarkesh Patel** _00:12:41_

They get hauled in front of Congress. It's not just because they made a sin of commission.

There's one answer where it's because they touched the problem. There's another where it's because they did it better than the government could have. Those seem like two different answers.

**Patrick McKenzie** _00:13:01_

You touched the problem so you've immediately taken liability for any number of sins of omission. Even at the scale of the largest companies in the world, you have not allocated infinite resources to this problem. Also, stealing a march on the government and embarrassing us will be held against you.

You can point back to the [Cambridge Analytica thing](https://en.wikipedia.org/wiki/Facebook%E2%80%93Cambridge_Analytica_data_scandal). Cambridge Analytica is shorthand for this one time back in the day when the news media in New York and the government in DC convinced themselves that a small team of people, with a budget of approximately $200,000, [rooted](https://en.wikipedia.org/wiki/Superuser) the United States presidential election.

Rooting the United States presidential election, perhaps on behalf of a foreign power, would be an enormously consequential thing. Good thing that did not happen in the world that we live in. However, people believe very passionately in that narrative. As a result of that narrative, they very aggressively attempted to clip the wings of tech and tech’s core businesses, like advertising.

**Dwarkesh Patel** _00:14:00_

There's so much that's great here.

We figured out that we couldn't delegate to big tech or any of the competent actors. The native infrastructure that we had — that was specifically earmarked for dealing with public health emergencies — was extremely incompetent to the extent that Discord servers vastly outperformed them.

Suppose that public health is not uniquely incompetent among the different functions that the government is supposed to perform. Those functions also don't get tested until the actual emergency is upon hand.

Say the president hears this and is concerned that the people running responses to nuclear bombs or earthquakes aren't up to snuff. Is there some stress test that you could perform on these institutions in order to learn whether they're competent or not, before the thing actually happens?

**Patrick McKenzie** _00:14:57_

Look at the experience of the last hundred years, or back to the [flu pandemic in 1918](https://en.wikipedia.org/wiki/Spanish_flu). A vastly less wealthy and less technologically sophisticated nation — with many fewer people involved in the actual fixing of this problem — competently executed on nationwide vaccine campaigns and other various measures.

We should be urgently concerned with what has decayed institutionally since then. If you had just given health departments this kind of vanilla vaccination campaign, maybe they would have done better than they actually did. I'm not positive about that.

Here I have to stop for a disclaimer. I think people in county health departments did real important work. They probably did work that saved lives on the margin. I do not think the United States should be satisfied with our performance in 2020 and 2021. We should be very dissatisfied and we should get better for the future. That requires recognizing that we underperformed by a lot.

There was a political decision made that the successful [administration of vaccination](https://en.wikipedia.org/wiki/COVID-19_vaccination_in_the_United_States) was not going to be measured solely by saving lives. The prioritization schedule that we came up with was byzantine and complicated. It routinely befuddled professional software engineers and health administrators. I could not diagram it out on a whiteboard even if you paid me a million dollars to get it right the first time.

That was all downstream of the United States' political preferences. Schedule 1A versus 1B versus 1C was in the first five seconds of the discussion dictated by medical necessity. Immediately after that it became about rewarding plums to politically favored groups. One of the complexities of this is that the pharmacies and healthcare departments are not set up to discriminate along the axes of whether one is politically powerful or not.

That is not a thing that they have to do in most vaccination campaigns. That’s not a thing that they have to do on like the typical Tuesday of providing medical services. We asked them to do this radically new thing, which is in part responsible for the failures that we had. If we had had a much simpler tiering system, we would have had more than 25% of the shots successfully being delivered in the state of California in January of 2021.

**Dwarkesh Patel** _00:17:26_

For people who are not aware, what was the political tiering system that you're referring to?

**Patrick McKenzie** _00:17:30_

Oh, goodness. This was different in different places. Confusingly, different places in the United States use the same names for these tiers for different people. In the state of California, Tier 1A comes before 1B comes before 1C comes before Tier 2, et cetera.

1A changed over time on a day-to-day, week-to-week basis, sometimes in mutually incompatible ways at the same time. It was an entire mess. At the start, [Tier 1A](https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/CDPH-Allocation-Guidelines-for-COVID-19-Vaccine-During-Phase-1A-Recommendations.aspx#:~:text=During%20Phase%201a%20of%20allocation,or%20long%2Dterm%20care%20settings.) was for healthcare professionals, a few others, and people above the age of 75. No wait, we'll change that to 65.

Tier 1B was where we put a few favored occupational groups and some other folks. Tier 1C was for people who doctors think will probably die if they contract COVID unvaccinated, but who have not appeared in group 1A or 1B yet.

Who got 1A? Healthcare professionals, like doctors administering the vaccine. That sounds pretty reasonable. Also, veterinarians. Were veterinarians urgently required by society at the time? Not so much. It was because the California Veterinarians Association is good at lobbying. That isn't just me alleging that. They sent [a letter out to their membership](https://media.kalzumeus.com/vaccinateca-wip/Vaccine-Status-Update-1-8-2021-1.pdf) saying, "we are so good at lobbying, we got you guys into 1A. Congrats and go get your vaccine now." I have that on my website.

Tier 1B. School teachers were classified as Tier 1B. Why? Go figure.Teachers’ unions have political power in the state of California. They said, “we'll accept not being in 1A, but we are going no lower than 1B.” Probably no one in that meeting ever said, "I definitely think that 25-year-old teachers who are currently under stay-at-home orders should be in front of people who will die if they get COVID." But we made that choice.

**Dwarkesh Patel** _00:19:23_

In your article you discussed that the consequence of this was not only the misprioritization of the vaccine. The bureaucracy around allocating it according to these tiers resulted in 75-year-olds not having the capacity to fill out the pages of paperwork required to decide what tier you're in.

**Patrick McKenzie** _00:19:40_

The state of New York commissioned a consultancy to administer to 75-year-olds a 57-page web application. It required uploading multiple attachments to check for their eligibility. Talk with a technologist if you don't believe me. We try to remove everything from a webpage so that people can successfully get through it.

If you can make it two to four form fields, that's already taxing people's patience. You are asking people — who might be suffering from cognitive decline or are less comfortable in using computers — to do something which would literally tax the patience and cognitive abilities of a professional software engineer.

That wasn't an accident. We wanted to do that. Why did we want to do that? It was extremely important to successfully implement the tiering system that we had agreed upon. Why was it extremely important to implement the tiering system? Because that was society's prioritization. Was that the correct prioritization? Hell no.

**Dwarkesh Patel** _00:20:36_

Can we just count off everything? It's enraging not only because people died, but because nobody talks about it. There are all kinds of controversies about COVID, about whether vaccination had side effects, whether the masking orders were too late or too early. The main thing should be whether we got vaccines in people's arms on time because of these political considerations.

**Patrick McKenzie** _00:21:10_

Can I jump in with one bit of optimism? We achieved something incredible. We got the first cut of the vaccine [done in two days](https://www.businessinsider.com/moderna-designed-coronavirus-vaccine-in-2-days-2020-11#:~:text=Moderna's%20groundbreaking%20coronavirus%20vaccine%20was%20designed%20in%20just%202%20days&text=The%20FDA%20granted%20emergency%20authorization,against%20COVID%2D19%20in%20trials.) as a result of [many decades of science](https://en.wikipedia.org/wiki/MRNA_vaccine) done by very incredible people. We successfully got that vaccine productionized in a year. We should have gotten it productionized in far less than a year. Still, the fact that we were able to do it in one year and not three was enormously consequential. We should feel happy about that.

We should be a little annoyed that we didn't have better protocols at the FDA and other places to get that vaccine prioritized for testing much faster. We should be quite annoyed at the fact that that was a political football. People probably made decisions that pessimized for human lives and optimized for defeating a non-preferred political candidate.

**Dwarkesh Patel** _00:21:53_

You’re talking about the fact that the vaccine was announced the day after the election results or something, right?

**Patrick McKenzie** _00:21:58_

Yes, I'm basically subtweeting that. I strongly believe that was a political decision, but I'm just a software guy.

**Dwarkesh Patel** _00:22:06_

There was a particular kind of craziness that we had during 2020 and 2021 about equity and wokeness. How much was that uniquely responsible for the dysfunctions of this tiering system and geolocation/redlining? Basically, if this happened in another year when there wasn't a bunch of cultural craziness, would it have gone significantly better?

**Patrick McKenzie** _00:22:31_

It's difficult to ask that question. We were clearly in a unique time in 2020 and 2021. Yet, point to me a year in American history in which American society was truly united and had no social issues going on. If people counterfactually point to say, World War II, I will say read more history there.

Be that as it may. Was it the case that strong societal feelings in the wake of [George Floyd's death in 2020 and the racial reckoning](https://en.wikipedia.org/wiki/George_Floyd_protests) strongly dictated policy? Yes. That's a positive statement rather than a normative statement. That is absolutely the case.

There's this thing we often say in the tech industry called [bike shedding](https://en.wikipedia.org/wiki/Law_of_triviality). If you're building a nuclear power plant, many people cannot sensibly comment on what is the flow rate through the pipes to cool a nuclear reactor. However, if you build a bike shed next to the nuclear power plant, it's very easy to have opinions on the color of the bike shed. So in the meetings about the nuclear power plant, you will have a truly stupid amount of human effort devoted to what colors you should paint the bike shed.

It is very difficult for most people in civil society to successfully inject a vaccine into someone's arms, to successfully manage a logistics network, to successfully build a nationwide information gathering system, to centralize this information and pass it out to everyone.

We aggressively trained the entire American [professional managerial class](https://en.wikipedia.org/wiki/Professional%E2%80%93managerial_class) in decrying systemic racism. To be clear, it is a problem.  The American professional managerial class essentially calls all the shots in the U.S. system. Any discussion about what we should do with regards to information distribution will almost invariably get bent to, “I have no particular opinions on server architecture here and nothing useful to comment, but what's our [equity](https://en.wikipedia.org/wiki/Diversity,_equity,_and_inclusion) strategy?”

The equity strategy dominated discussions of the correct way to run the rollout to the exclusion of operationalizing it via medical necessity. People brag about that fact. That fact is enormously frustrating to me. If you say it with exactly those words and emotional valence, people will say, “no, that's not exactly what we meant.” When they're talking to other audiences, they say, “no, this is absolutely what we mean.”

**Dwarkesh Patel** _00:25:01_

Maybe the culprit here is a [scarcity](https://en.wikipedia.org/wiki/Scarcity_/(social_psychology/)) mindset. We cared more about proportions rather than just solving the problem.

**Patrick McKenzie** _00:25:14_

This was one of those few times when we were up against a genuine scarcity constraint. The physical reality was that there were a scarce number of vials. We needed a prioritization system. Some people who urgently needed the vials were not going to get them first. Everyone was going to get them eventually. However, our political system's mad rush to dole out favors in prioritization for those first vials exceeded the actual distribution and injection of the vials as a goal.

California reported to the federal government that it was only successfully injecting 25% of its allocation. It had the most desirable object in the history of the world. Rather than adopting any sensible strategy to get it into people's arms, it was bickering over who should get it first. We should be outraged about this, but we're mostly not.

**Dwarkesh Patel** _00:26:05_

I don’t even know what to ask next because it’s so obviously outrageous. To me, there's no clear answer about why there isn't more outrage about it.

Also, the solution isn't obvious. It’s not clear to me that we’ve learned the lesson for the next pandemic, let alone for a different emergency. For an isomorphic emergency, would our state capacity be better?

You mentioned how 100 years ago, we might have been able to deal with this problem better. What changed?

**Patrick McKenzie** _00:26:39_

America used to do something when the federal government lacked state capacity for something. It’d identify who in civil society or private industry had capacity for this. Then they'd say, "congratulations. By order of the president you're now a colonel in the United States army. What do you need to get it done, sir?" That option was available but not taken.

I will play no fights in either of the two administrations. Both individually made terrible decisions. But plausibly, a more enlightened counterfactual administration could have gone to Google and said, "who's your best person for solving this data problem? Will they accept a commission as colonel? Great. Here's an order from the president. Your swearing-in ceremony starts in 30 seconds. You'll present your project plan tomorrow."

Again, the successful project plan was actually created by rank amateurs on Discord in a couple of hours. This is just one part of the huge vaccination effort. You could imagine going to Amazon and saying, "hey Amazon, we hear you're good at getting packages from A to B. This package has a really hard challenge. It needs to stay cool during delivery. That’s a totally unsolved problem in material science, right?" Amazon would say, "we literally do that every day."

They say, “back in December, people were saying on the news this would be an unprecedented logistics challenge because the vaccine has to be kept at ultra-low temperatures.” These are the same temperatures at which milk is transported. We already understand [cold chain logistics](https://en.wikipedia.org/wiki/Cold_chain).

So Amazon would correct that misperception. They say, “oh you guys seem to know what you’re doing. We have an absence of that here. Congratulations, here’s your colonel uniform in the US military. Now we are going to give you a CSV file everyday. Interface with this other colonel from Google on where this thing needs to go. You get it there on time everytime. If you can’t get it there on time everytime, call the White House and we will find you political cover.” That’s what a functioning system would have done.

Granted, the American system is dysfunctional in its own way. We've also underexplored international comparisons in the last couple years. I don't know if any country anywhere, with vastly different political systems, is happy with their outcomes. Some were obviously vastly better than others. There are journals of comparative international politics. Why are those journals writing anything but analysis of who succeeded at what margins and who didn't? What do we learn about about the proper functioning of political systems, civil society, and the United States considered as one hugely complex machine..

**Dwarkesh Patel** _00:29:27_

That's a really interesting point. I actually asked the [Tony Blair Institute](https://www.dwarkeshpatel.com/p/tony-blair). They were recommending different ways of distributing the vaccine to the British government. They made the obvious recommendation that they should give everybody one dose now and then do the second dose later.

There were obvious things like this that would have saved lives. The British government didn't do a good job there. No government… it's actually a very interesting question. There are governments all across the world that have very different political systems. They hopefully have different infrastructure already in the mix of this.

Why did nobody get this right?

**Patrick McKenzie** _00:30:02_

The catchphrase for this was ["First Doses First."](https://marginalrevolution.com/marginalrevolution/2020/12/double-the-inoculated-population-with-one-dose.html) This wasn't the procedure in many nations with many smart people, including the United States. Sometimes you can trace policy back to individual blog posts. In this case, I believe it was Alex Tabarrok on _Marginal Revolution_ who was right. This is very obvious and overdetermined. If we want to win at this, First Doses First is objectively the correct policy.

This idea ping-ponged around the political system for a while. They talked to medical experts who eventually agreed. This is the equivalent of saying you should probably consume calories at some point in a typical week. It’s better than not consuming calories. “We checked with medical experts, and after six weeks of meetings, they definitely agreed eating beats not eating for living. So we're going to do that now.”

On one hand, it's a genuine strength of the United States that we didn’t just follow some relatively unknown person on the internet who wrote a 2000-word blog post in order to stop doing stupid things. We could have stopped doing the stupid things sooner though.

**Dwarkesh Patel** _00:31:25_

That doesn't answer the question of why nobody got it right. Is there something particular to the late-stage bureaucracy we have? Maybe another country with a fresher system or a more authoritarian model that can crack down would do better. But they did abysmally as well, often making errors worse than America's. There are so many countries, Patrick. Why didn't any of them get it right?

**Patrick McKenzie** _00:31:51_

I'm under-informed on much of the international comparison, partly because in 2021 I was sort of busy. However, I remember Israel, for various institutional reasons, having a broadly functional response, particularly around end-of-day shots. End-of-the-day shots are a minor issue in the grand scheme of things, but they’re a good quick heuristic for assessing if a country has good epistemics on this at all.

The physical reality of COVID shots is that there are 5, 8, or 10 shots in a single vial. That single vial goes bad after 12 hours. That's a bit of an oversimplification, but for regulatory reasons we have to pretend it goes bad after 12 hours. It can't be resealed. If you vaccinate two people then the other shots are on a timer. They will decrease in value to zero after the remaining hours and then get thrown in the trash.

Here's a quick question to test if you're a rational human being. At the margin, would you prefer giving a shot to the most preferred patient in your queue, who needs it for medical reasons, or to the trash can? You'd prefer the most preferred patient. Here’s a follow-up question. Would you prefer giving it to the least preferred patient or the trash can? You'd still give it to the human rather than the trash can.

Israel adopted the policy that if shots were expiring, they'd forget the tiering system and anything else. They'd literally walk out into the street and say, "I've got the COVID shot. I need to administer it in the next 15 minutes. Who wants it?" In the United States, we had a policy ban on doing that. We said no. To protect the integrity of the tiering system and embrace our glorious cause of health equity, you should throw that shot out. This policy was stupid and it was announced by governors proudly in December in front of news cameras.

A couple of weeks later, reality set in. People told them, "sir, it turns out that throwing out the vaccine is stupid." The governor didn't go on the nightly news again to say, "I gave a very confident policy speech a month ago in front of this news camera. I said that I would prosecute anyone who gives out end-of-day shots—”

**Dwarkesh Patel** _00:34:23_

He literally said that. He literally said that.

**Patrick McKenzie** _00:34:26_

Oh man, this is almost a direct quote. You can see the actual direct quote in my previous writing on this. “I will not just prosecute people. I will aggressively try to maximize the reputational impact on your firms and your licenses.”

We were pointing metaphorical and, when it came down to it, literal guns at physicians in the middle of a pandemic for doing unauthorized medical care. It’s crazy. When the system corrected, it did not correct all the way. The governor did not go out and say, “hey, that thing I said a month ago was effing insane. I take that back and apologize.” No, it was like, “okay, we're going to quietly pass out the word. That's no longer the policy, but we don't want to own up to the mistake.”

People, say in the regulatory departments of pharmacies, make rational decisions based on the signals that you are giving them. The rational decision a pharmacy makes is not, “okay, we've been quietly passed the word that the old policy is persona non grata. But can we really trust the quiet word here? Do we trust that this actor is not going to change their mind in two weeks and consequence us for something we authorize today? Just throw out the shots.”

Pharmacies did not cover themselves in glory. Some individual pharmacists did, but pharmacies institutionally did not. Pharmacies were thinking, “we deliver almost all the medications for almost all the diseases routinely in America. We cannot blow up either that position of societal trust or our business results over one drug for one disease.”

They decided to throw out the shots and make sure they could still deliver medical care in California tomorrow. I understand how that decision was made. We should not endorse that decision. There were individual acts of heroism by particular pharmacists who essentially said something like this to us when we called them and asked about the procedure for getting the shot.

"Okay, an individual like the one you just described cannot formally get the shot right now. I would tell that individual to go to the county website and tell whatever lies are necessary to get an appointment with me. They come in for an appointment and I will inject them rather than verifying the lies that were on the appointment card because basically eff the rules. I swore an oath."

**Dwarkesh Patel** _00:36:48_

Honestly, I don't know where to begin with some of these things. I want to understand a bunch of that.

First of all, 25% of the vaccines that were allocated to California were actually delivered in people's arms? Literally the entire world economy was bottlenecked on this, right?

**Patrick McKenzie** _00:37:06_

Here’s another funny anecdote. I asked some people in positions that might know, "how real do you think that 25% number is?" They said, "the good news is in addition to being incompetent at delivering the vaccine, we're also incompetent at counting.” So it was probably a bit of an undercount.

I'm like, "oh so the good news is the true count was like 100 percent or 95 percent or something?" They were like, "no, not nearly close to that, but we got better at counting after the governor yelled at us because he was embarrassed. We were the 40th state in the nation.”

**Dwarkesh Patel** _00:37:36_

It’s literally just counting the item, a bottle. Where's the thing that is going to rescue us from the thing that is destroying the world?

**Patrick McKenzie** _00:37:42_

Let’s say you ask someone deep in the bowels of pharmacies' accounting departments, "could you, by the end of business today, give us a count of how many bottles of aspirin the pharmacy has physically in the world?" By the end of the day, they would have a shockingly accurate number for that. It wouldn't be exact, but it would be shockingly accurate relative to that number being truly millions.

If you could say, "break it down by address, please. Where are they physically present in the world?" That’d be an easy problem. Managing inventories of drugs, that's what we do. The United States could not do that. It did not perceive that to be an urgent problem to be solved.

**Dwarkesh Patel** _00:38:19_

I do want to ask you about the actual finance and software stuff at some point, but this is such an important topic. The world is brought to a stand still. We still haven't learned the lesson. I'm just going to keep going on this topic because I still don't understand.

Here's another question that's related to this. You have many rich tech industry friends. I read your article and you're saying, “I'm filling out these grants for $50k a year. That's taking up all my time. I'm trying to raise a couple hundred grand a year, a couple tens here.”

I'm thinking to myself, how is this not as trivial a problem as, “hey XYZ, if you give me money that you can find between your couch cushions, we will save thousands of lives and get the world economy back on track.” How is raising money for this hard? Or why was it hard?

**Patrick McKenzie** _00:39:07_

Again, trillions of dollars are on the line. The United States is spending tens of billions of dollars or more on its COVID response strategy. The true biggest issue is why has it come down to Patrick McKenzie's ability to fundraise in the tech industry for us to have a system here?

Bracketing that, the tech industry underperformed my expectations for what it should have accomplished here. There were some bright spots and less bright spots with regards to the fundraising project. For those of you who don't know, the total budget of this project was $1.2 million. It’s not quite couch cushion money, but it’s not large relative to the total amount of resources that the tech industry can deploy on problems.

I looked at my email this morning to refresh my memory. I'm not going to name people, but they're welcome to claim credit if they want to claim credit. I emailed the CEO at a particular company, "hey, I saw you like to tweet about this on Twitter. I'm essentially raising a [seed round](https://en.wikipedia.org/wiki/Seed_money) except for a [501(c)(3) charity](https://en.wikipedia.org/wiki/501/(c/)/(3/)_organization) and we urgently need money for this. Here's a two page memo."

I sent that email at 4:30 p.m. California time. He got back to me. There were some internal emails routed to this person and then to that person. “Hey run that by blah, blah, blah.” 9:30 the next morning, he said, "I'm personally in for $100,000 out of my own pocket. My banker is going to contact you.” The wire cleared the same day. So yay for that.

On the less yay side, tech is not exactly a stranger to having bureaucracies. In some cases, it was a matter of "oh indicatively, we want to support that, but we have a process" and that process went on for six weeks. By the time six weeks was over, it was May.

By May, most people in the professional managerial class who had prioritized getting a vaccine for themselves and their loved ones had succeeded at that. They said, "okay, the vaccination supply problem is pretty much solved, right?" I'm like, “no, it is not solved right now.” It is solved for the people who are smartest about working the system in a way it was not solved for even them back in January. But there are many people who are not yet vaccinated.

They’d say, "that's a vaccine hesitancy issue." No, it is not merely a vaccine hesitancy issue. It is still the case that there are logistical problems. It is still the case that people don't know that you can just Google the vaccine now. It is still the case that around the edges of the American medical system, in places that are underserved, people don't have it or they can't get transportation, etc. You should continue funding this team for the next couple of months so that we can do what we can around the edges here.

Again, people can do what they want with their own money. I understand that charitable funders have many things. I was told, “relative to the other places we can put money to work in the world, further investment in the American vaccine supply situation as of May and looking forward, it doesn't make sense for us. Could you do it in another nation?”

We said, “okay, we're the American effort. We have some advantages here. We would not have them in another nation. We did talk to people there. We tried to see if we could help a team there or go there, etc. But we don't see that there's a path to positively impacting the problem there in a way that there's manifestly a path to positive impact here.”

We lost that argument. We didn't get the money. The last $100K in was my daughter's college education fund.

**Dwarkesh Patel** _00:42:34_

My God.

I agree that it shouldn't be up to tech to solve this huge society-wide problem. But given that nobody else was solving it, I still don't understand. Have you gone back to any of them? Have any of them reflected like "yeah, maybe I should have just written you a million dollar check and saved you all this hassle so you could have gone back to business."

**Patrick McKenzie** _00:42:59_

Ultimately I'm the CEO. Responsibility for fundraising lies with me. I've thought a number of things about how I could have done better. How could I have strategized? I did not stop fundraising efforts, but I stopped lighting up new conversations for a number of weeks. I thought, “okay, we've got the $2 million that we need to run this till the end of August.” That's my internal target for the point at which it doesn't quite stop being useful, but it starts actually being a question on the margins. It's not a question until the end of August. Could I've done better? Probably.

There’s some of the folks in the broader [effective altruist](https://en.wikipedia.org/wiki/Effective_altruism) community. I'm not a member, but I've read a lot of stuff that they have written over the years. I broadly consider them positive. They are the "but for" cause of VaccinateCA. Ask me about that in a moment. Some EA funders talked to me after my piece about it came out. They said, "this is physically painful to read. We wrote bigger checks with less consideration to projects that had far less indices of success. Why didn't you just ask us for money?"

The answer there was twofold. One, I thought I had high quality introductions and a high quality personal network to people who are likely already going to fund it. So I didn't light up additional funding sources. And two, this is a true answer, I'm a flawed human who has a limited number of cycles in his day. I was running a very complex operation. It literally didn't occur to me, “hey, maybe those people that have been making a lot of noise about writing a lot of money for pandemic checks would be willing to write a pandemic check.”

That was not entirely an irrational belief for me because I had reached out to people who are making a lot of noise about writing money for pandemic checks. They said, "not in the United States, not in May." I thought, “oh, if I light up a conversation totally cold with someone now, it's likely to just get a no again.” I should try to scrimp and save and break the piggy bank for my daughter's college education fund. By the way, she'll go to college folks, no worries. But it's how far down the list of Plan A, Plan B, and Plan C. We were down to Plan C at that point.

**Dwarkesh Patel** _00:45:02_

Just to be clear, I'm definitely not blaming you. It goes back to the Copenhagen interpretation.

**Patrick McKenzie** _00:45:07_

No, but you should blame me a little bit because I should be rigorous about my performance.

**Dwarkesh Patel** _00:45:11_

You go back to commission versus omission. It's the exact same reason that we shouldn't have blamed Google if they got involved, did it themselves, and maybe made a mistake. Like come on, to remove the bottleneck that was basically stopping all global economic activity and causing millions of deaths. you had to take money out of your daughter's college fund. It's so insane.

**Patrick McKenzie** _00:45:42_

There's a positive takeaway here. There is one tiny actor who understands that he has unitary control over some decisions, and who is capable of betting boldly on those without a huge amount of process when it is important to bet boldly on things. Not to toot my own horn here, but this is literally what happened.

On the first day, we're getting in Discord together and there's a bunch of infrastructure we have to sign up for. We have to get hosting, etc. There is an annoying mechanical step at this point where you have to put down a credit card, for a potentially unbounded expense.

People were like, “there's a list of things that we want to do. Since there is no money here, I'll take this one and you take this one.” After I heard this conversation go on for two minutes, I said,”this is not a conversation we should be having. Here is a debit card for my business which I've just spun up on the backend. This is literally my job. It has $10,000 on it. Spend the $10,000 on anything that accelerates this project. There is no approval process. Don't get a receipt. Don't worry about the paperwork right now.”

Why did I do that? “The information about where hospitals exist and what their phone numbers are is probably [scrapable](https://en.wikipedia.org/wiki/Web_scraping) from the internet for free. Or we could buy a commercial database, but that's a stupid amount of money. It's like $2,000.” I'm like, “relative to the importance of this project, $2,000 is a trivial amount of money. Just spend the $2,000 immediately rather than spending four hours writing a scraper.”

We don't think about that in government procurement and in charities. We have some sacred virtues like, “you must minimize waste. You must minimize opportunities for corruption. You must maximize for funders’ line item support of individual things that charities buy.”

Those sacred virtues conflict with winning. At the margins where they conflict, we should choose winning. We should choose human lives over reducing corruption. One of the few things we are reflecting on is the tremendous amount of waste and fraud that happened with [PPP loans](https://en.wikipedia.org/wiki/Paycheck_Protection_Program) and other [pandemic stimulus](https://en.wikipedia.org/wiki/CARES_Act) things. I'm not just saying this to be contrarian, folks. We should be glad there was waste in COVID stimulus. If there was no waste, we were clearly not choosing the right margin to focus our efforts on.

**Dwarkesh Patel** _00:48:16_

I want to clarify this for people who don't have context on how much money typically goes around in Silicon Valley. They think, "oh, $1.4 million. How hard should that be to raise?" If you right now, given your reputation, literally tweeted out, "I'm not going to tell you my idea but I'm raising a $50 million seed round," that's going to get filled.

People don't understand. I have friends who are 16 years old who have some [GPT wrapper](https://learnprompting.org/blog/2024/2/4/gpt_wrappers) and they don't have to worry twice about raising $1.4 million.

**Patrick McKenzie** _00:48:48_

Not trying to brag folks, just telling you the reality of Silicon Valley. I misapplied some of the  knowledge I have of how seed funding would work if I attempted to raise for a for-profit company.

I thought originally, we're probably going to be charitable, but I'm going to pitch this to people as essentially like a seed investment. They expect to spend all the money as quickly as possible and go to zero, while driving the [total addressable market](https://en.wikipedia.org/wiki/Total_addressable_market) of the company to zero. I'm bummed this is what passes for humor with me.

I told folks pretty confidently in the first couple of days, “I'm pretty sure I can get us $8 million.” Then I was actually able to deliver on $1.2 million after far more tooth pulling. But yes, descriptively, if I was asking for a seed stage investment and I wanted to get $8 million wired by tomorrow, I could probably do that.

That is a civilizational inadequacy because can you literally get $8 million for a blank check for something that has a profit motive behind it. If I write on the check, “hey, we want to fix the manifest inability of the United States to figure out where the COVID vials are,” that blank paper becomes less valuable.

On reflection, maybe I shouldn't have told people, and said, "oh, the blank check company was this thing and we're making it a 501(c)(3)." There are maybe some ethics issues in that, but the ethics issues are less bad than allowing people to die.

**Dwarkesh Patel** _00:50:16_

A recent episode I released was with [a former AI researcher](https://www.dwarkeshpatel.com/p/leopold-aschenbrenner) who thinks that the field is progressing in such a way that you will need to nationalize the research in order to protect American national security. I hear what you’re saying about the inability of the government to keep track of vials of COVID vaccines or to get them in people's arms.

For any other emergency — whether it’s AI or the fallout of a nuclear war — should we just discount any government response to zero? If your plan requires some sort of competent administration by the government, should that be discounted to zero? It has to be something on the side.

**Patrick McKenzie** _00:51:09_

Discounting to zero is the opposite of wisdom here because we didn't accomplish zero. We accomplished an extremely impressive thing in aggregate. It vastly underperformed the true thing that we were capable of. You have to keep both parts of the equation in our minds at the same time.

People in tech need to become radically more skilled at interfacing with government. To the extent that we have some manifest competency issues in government right now, we can't simply sit out here and gripe about this on podcasts, etc. We've got to go out and do something about it.

I think it's been reported that there was a meeting among tech leaders early in the vaccination effort where a bunch of people got in a room and were like, "this is going terribly. I hope someone fixes it." "I hope someone fixes it" is no longer a realistic alternative. We have to be part of the solution.

It's partly about having higher fidelity models for how Washington works than simply, "oh, they're bad at everything." It is important to understand that the government has some manifest competence issues. It's also important when working with the government to understand that telling the government to its face, "you have manifest competence issues" is not the maximally effective way to keep getting invited to the meetings.

I was very religious about not criticizing anything about this Californian response effort in 2021 because we needed to be in the room where it happens. That was a choice made. Am I 100% happy with that choice? No, but we kept some relationships that we really needed. I'm not saying don't criticize the government, obviously. Be strategic about that sort of thing. Play like you are attempting to win the game.

On the government side, one thing we need is dispelling the massive “ugh” field that surrounds software. This is going to be a part of the future, whether you like it or not. We need to get good at it. We can no longer accept incompetence at this as the routine standard of practice in Washington.

Secondly, it is enormously to the United States’ credit that we have an extremely functional, capable tech industry. Maybe we shouldn't treat it like the enemy. I’m just putting that out there. Again, this is a thing the United States has done before. There are laws in place. There are decades of practice. We could put a colonel's uniform on somebody. Think seriously about doing that next time.

Do I think we have institutionally absorbed all the correct lessons from this? No. When I see after action reports, they praise a lot of the things that people think are very important for maintaining their political coalition. These are things which were either not productive or anti-productive.

They fail to identify things that were the true issues. To the extent that they identify things that were the true issues, the recommended action is, "I hope someone fixes this next time." That’s no longer sufficient, that the default case is that the ball will be dropped.

Those of us who were involved in VaccinateCA kind of dread what we call the [Bat-Signal](https://en.wikipedia.org/wiki/Bat-Signal). God willing, there will not be another worldwide pandemic killing millions of people as long as we live. If there is one, we know what numbers to text to get the band back together. Society should not rely on us as Plan A. How did this happen?

**Dwarkesh Patel** _00:54:51_

The point about griping on a podcast, that's definitely what I'm doing. Maybe you’re too humble to say this for yourself. I do want to commend you for this. There are very few people who would do this.

You tweeted it out. There are probably other projects that other people could have taken up that are not taken up. In this case, you tweeted it out. You saw that there was a thing that could be done and you did it. You quit your job and you did this full-time. The reason you had to dip into your kid's college fund was because somebody who had promised a donation didn't follow up on it, right?

**Patrick McKenzie** _00:55:25_

Effectively every time we had a verbal green light with regards to money, I would advance the company, the charity… Charities are companies, by the way. I don't know if that is obvious. It was called Call the Shots Incorporated.

I would advance Call the Shots the money that was soft committed, before the money would actually arrive in the bank on the theory that this accelerates our impact. We should always choose acceleration over other things such as minimizing credit risk.

Some of the people who had soft committed did not actually end up wiring money at the end of the day. Shoot. My choices now are either don't run the last payroll or do run the last payroll and do not recover the money I've advanced the company. I said “okay, do run the last payroll.”

**Dwarkesh Patel** _00:56:19_

Did you end up recovering it in the end?

**Patrick McKenzie** _00:56:20_

No, it ended up being a donation from me personally to the effort.

**Dwarkesh Patel** _00:56:25_

What the fuck?

**Patrick McKenzie** _00:56:27_

That is the least important part of the story folks.

**Dwarkesh Patel** _00:56:29_

Sure. But overall… kudos obviously isn't enough to convey what I mean to say here. I'm glad you did that and I'm grateful. You saved a four-figure amount of lives. It’s hard to plot that on a graph and make sense of what that means.

**Patrick McKenzie** _00:56:49_

To the extent kudos are deserved by anyone, it’s Karl Yang for taking up the torch and finding 10 people in the tech industry who would jump into something at nine o'clock. It’s those 10 people, the other board members, the hundreds of volunteers, the team of about 12 people who worked on it full-time — and very full definitions of full-time, virtually ceaseless — for five, six months.

There were other projects in civil society. There were many people doing this as their day jobs. The American response effort is not one small group of people anywhere. It's the collection of all these things bouncing off of each other.

I'm happy about our individual impact. I'm happy that, descriptively speaking, if you Googled for the vaccine at any point before a certain day, there was no answer. After that day, there was an answer. That answer came from us.

I’m a little dissatisfied that it didn't come from people with vastly more ability to have caused that much earlier. But the ultimate takeaway is not about this little tiny piece of the puzzle. How can we make the total puzzle better next time?

**Dwarkesh Patel** _00:58:58_

Let's talk about some finance. In addition to saving thousands of lives with VaccinateCA, what you've been doing over the last year or two is writing this very excellent finance newsletter called _[Bits about Money](https://www.bitsaboutmoney.com/)_. You explore the plumbing in the financial system.

Here’s my first question about this. [Crypto](https://en.wikipedia.org/wiki/Cryptocurrency) at its peak was worth $3 trillion or something like that. From the crypto skeptic perspective that you have, how do we think about this number? What does it represent? Was it just the redistribution of wealth from dupes to savvy people?

To the extent that useful applications didn't come out of this $3 trillion, what does it represent?

**Patrick McKenzie** _00:59:40_

I have two broad perspectives on this. People often treat the market cap of something as implicitly like some sort of cost on society. The true cost of crypto on society has been this. Anytime one engages in attempting to do productive enterprise, some actor in society has said, “okay, I will stake you with some of society's resources. These resources are [rivalrous](https://en.wikipedia.org/wiki/Rivalry_/(economics/)). They cannot be applied to any other things society needs. I do this in the hope that you will produce something that is worthy of being staked with this.”

How much have we spent on crypto? Not on trading tokens around, but I mean building infrastructure and spending rivalrous resources that we can't get back. There’s [GPUs](https://www.investopedia.com/tech/gpu-cryptocurrency-mining/) or [ASICs](https://www.investopedia.com/terms/a/asic.asp) or electricity that could have gone to other things in China, but went into [mining](https://en.wikipedia.org/wiki/Bitcoin_protocol#Mining). There’s the time of talented and intelligent people that could have been building other software products but were instead building crypto. That number is in the tens of billions or hundreds of billions of dollars.

What do we have to show for that tens of billions or hundreds of billions of dollars? I am very crypto skeptical and I could give you an answer to that question. Crypto fans would not like to hear it from me. So I prefer [Vitalik Buterin's articulation of this question from 2017](https://x.com/VitalikButerin/status/940744724431982594). At the time it was $0.5 trillion, a trivial number only $500 billion. He asked, and I'm paraphrasing, "have we truly earned this number? How many of the unbanked have we actually banked? How many distributed applications have a meaningful amount of value doing something which is meaningful?" He has about [six other meditations on this](https://vitalik.eth.limo/).

Crypto folks certainly aren't accountable to me. In some manner, you're not even accountable to Vitalik even though he's clearly a leading intellectual in the community. You're accountable to producing positive value in the world. What is the answer to Vitalik in 2024? How many of the unbanked have we truly banked? What is the best use case for crypto right now?

Once crypto has a responsive answer that is sized anything like proportionate to the hundreds of billions of dollars resources that we've staked crypto with, then crypto people should feel enormously proud of that accomplishment. In some future where that hypothetically arrives, you have my sword. I will love your initiative. However, for the last many years we have been saying you can still get in early. You can still get in early because the value has not arrived yet.

That is my capsule summary on crypto 14 years in. We've staked a group of talented people who are very good at giving a sales pitch, with tens or hundreds of billions of dollars and look at what we have built. This would be a failure in any other tech company, a capital-F failure. Either radically pivot and unfail it or maybe we should stop continuing to stake you with money.

**Dwarkesh Patel** _01:02:46_

Here are two potential responses from the crypto optimistic perspective. I have some people who help me with the podcast who are around the world. I have a clip editor in Argentina. I have a shorts editor in Sri Lanka. I asked them, “how should I pay you?” I haven't prompted them and they say [USDC](https://en.wikipedia.org/wiki/USD_Coin). Maybe it wouldn't be that much harder for them to set up a [Wise](https://wise.com/) account, but it's notable that their first answer is a stablecoin.

**Patrick McKenzie** _01:03:27_

Absolutely, that is evidence. Some tech savvy people have a good payment rail. Well they have a payment rail that they did not have access to 15 years ago, but at the cost of tens or hundreds of billions of dollars. Counterfactually, one could have wanted to work on that payment rail specifically. Another way one could hypothetically have deployed $10 billion is on the best funded lobbying campaign in history in the United States to work on like [AML](https://en.wikipedia.org/wiki/Anti%E2%80%93money_laundering) and [KYC](https://en.wikipedia.org/wiki/Know_your_customer) regulation to allow easier transfers of money worldwide.

**Dwarkesh Patel** _01:04:00_

Why does it have to be compared against the best possible counterfactual use case? It's the sins of commission versus omission again. On the margin, it made things better.

**Patrick McKenzie** _01:04:09_

Don't judge it by hypothetical rules. Just keep in mind that hypothetical worlds might exist. Judge it by the actual realized utility at the moment relative to the amount of resources consumed.

**Dwarkesh Patel** _01:04:18_

Here’s the second point. Look at the [dot-com bubble](https://en.wikipedia.org/wiki/Dot-com_bubble) for example. Literally close to a trillion dollars were invested in laying out the fiber and the cable for this artifact that you now consider the most valuable thing that humanity has built. A lot of the companies that built this went bust.

There was a [bubble-like dynamic](https://en.wikipedia.org/wiki/Economic_bubble) where many of the investors who spent the capital to build out this infrastructure weren't paid back. They didn't see immediate use cases from what they'd built. The bubble had served as a [Schelling point](https://en.wikipedia.org/wiki/Focal_point_/(game_theory/)) to get things rolling in the future. That was hundreds of billions of dollars, a trillion dollars. With tens of billions of dollars, if something cool and useful comes out of it in the future, that's probably worth it, right?

**Patrick McKenzie** _01:04:59_

Cool. At what point do we get to say that didn't happen? At what date in the future do we judge whether someone has been right or not with respect to this. People in crypto have very confidently stated that this is the [next iteration of the internet](https://en.wikipedia.org/wiki/Web3) and this will revolutionize the world. Not just how payments are conducted, but it will be a fundamentally new computing architecture.

Okay, on what day do we compare notes on whether that claim was accurate or not

**Dwarkesh Patel** _01:05:33_

Does 2030 seem like a reasonable year? Or is that too far?

**Patrick McKenzie** _01:05:35_

It seems reasonable to me. Can I make a prediction of what is said in 2030?

“You can still be early. Crypto has created huge amounts of things, but it's not achieved anything near its true potential. Please invest in our new crypto startup.”

Let's check back in 2030, folks. Please [tweet at me if I'm wrong in 2030](https://x.com/patio11). I will happily eat crow. I want to eat crow. Crypto people are like, “how couldn't you be interested in programmable money?” I'm interested in programmable money, obviously. Money is programmable money.

My friends who have been trying to sell me on this since 2010 weren't wrong. This should totally smash my interests based on what I usually find intellectually edifying. I don't not find crypto intellectually edifying. There are actually some interesting things that have come out of the movement.

I find a [computer built in Minecraft out of redstone](https://www.youtube.com/watch?v=-BP7DhHTU-I) to be intellectually edifying. It's a wonderful educational device for people who don't understand how a CPU works. I'm not proposing to use the redstone-emulated computer in Minecraft to be the next computational infrastructure for the world. Fairly obviously, that will not work very well.

**Dwarkesh Patel** _01:06:52_

Here’s another answer of what the value is. We want some sort of hedge. I think this is actually a reasonable argument. I actually don't buy the capabilities unlocked by crypto, but I do buy the argument that we want some kind of hedge against the government going crazy and KYC/AML leading to state surveillance. All the compliance departments in the banks start seeing if you've been to [political protests](https://en.wikipedia.org/wiki/Canada_convoy_protest#Fundraising) and [de-banking](https://en.wikipedia.org/wiki/De-banking) you.

It may seem unlikely, but it's good to have this alternative rail which keeps the system honest. Given that there's an alternative, if things go off the rails this is a worthwhile investment. Society as a whole can't even count that low in terms of the other resources that it spends. It's a good hedge against that kind of outcome.

**Patrick McKenzie** _01:07:45_

I'm actually much more sympathetic to crypto people than they expect most people who have a traditional financial background to be. It is descriptively accurate that the banking system — and all companies which are necessarily tightly tied to the banking system, which might be all companies — are a policy arm of the government…

Whether people articulate that in exactly those words or not varies a little bit, but when you have your mandatory compliance training you'll be told in no uncertain terms that you are a policy arm of the government. I feel for crypto folks that say that this feels like [warrantless search and seizures](https://en.wikipedia.org/wiki/Warrantless_searches_in_the_United_States) of people's information in a very undirected [dragnet](https://en.wikipedia.org/wiki/Dragnet_/(policing/)) fashion.

I have somewhat complicated thoughts about this. The modern edifice of KYC and AML dates back to the [Bank Secrecy Act](https://en.wikipedia.org/wiki/Bank_Secrecy_Act) in the United States, which was in late 1970s. At the time, the US federal government was strictly [rate limited](https://en.wikipedia.org/wiki/Rate_limiting) in how much attention it could give to KYC and AML. Maybe because we thought we had very limited state capacity at the time, the government would make rational decisions and go after $10-100 million enormous white collar crooks and drug trafficking cartels a year. It would not surveil down to literally everyone in society.

However, the regulations we wrote and have continued to tighten over the years do effectively ask for transaction-level surveillance of every transaction that goes through a bank. This is the actual practice. This is not a conspiracy theory. I'm making nothing up, folks. The actual practice in banks is that they have about as many intelligence analysts as the American intelligence community has.

They get this scrolling feed of alerts generated by automated systems. For each alert, they go, “don't worry, don’t worry, don’t worry, don’t worry…” for millions of these alerts every day. Then for some tiny percentage, they say, “oh dear, this one might actually have been a problem. I'm going to write a two to four page memo and file it with the [Financial Crimes Enforcement Network](https://en.wikipedia.org/wiki/Financial_Crimes_Enforcement_Network).”

In all probability, no one is ever actually going to read that memo. We have an intelligence community-sized operation running in banks to write memos that no one ever reads. Some tiny portion of those memos will be useful to law enforcement in the future.

If you had explained that trade in a presidential debate in the 1980s, I find it extremely unlikely that any part of the American polity would want to buy that. Could we perhaps spend tens of billions of dollars on it? But we did that.

To that extent I'm extremely copacetic with crypto folks on this.

Point. A: This thing factually exists in the world. I agree with you that it does.

Point B: In an ideal world, this thing would not exist. I agree with you, there are very real privacy fears.

However, crypto has this habit. People who are good at sales have various sales pitches that they give to people. Actors within the crypto ecosystem will talk an excellent game about privacy as long as “number go up.” When you have to choose between being tied into the banking system — which is necessary for number go up — or you can choose privacy, they will say, “excellent, I choose number go up.”

**Dwarkesh Patel** _01:11:20_

But there are different protocols. You can use the ones that allow privacy if you care more about privacy.

**Patrick McKenzie** _01:11:27_

That is a very tiny portion of crypto.

**Dwarkesh Patel** _01:11:33_

I want to riff on what you were saying about the analysts. They have as many as would be in an intelligence agency. You have these apparatchiks who are connected to the government's policy, just analyzing each transaction. As soon as the government gets the competence to run an [LLM](https://en.wikipedia.org/wiki/Large_language_model) across each of these millions of queries…

**Patrick McKenzie** _01:11:54_

This is a legitimate worry. We have extremely low state capacity for this thing that we didn't think was important, successfully administering vaccines. But we do have extremely high state capacity with regards to running the security state. There are pluses and minuses there, but they have built some things that are extremely impressive technologically.

If they successfully manage to get their technological ducks in order and then just run a LLM on this data set that we've passively been producing… The implicit ongoing invasion of privacy is much worse than we baked into the system in 1980. Back then it would have been people going down to archives to look at things in microfiche to try to do this.

**Dwarkesh Patel** _01:12:40_

I'm not even necessarily making a point over crypto here. It's worth meditating on the fact that the default path for this technology is that a very smart LLM is going to be looking at every single electronic transaction ever. It's intelligent enough to understand the implications, how it connects to your other transactions and what's the broader activity you're doing here.

**Patrick McKenzie** _01:13:07_

Can we step back from crypto and finance for a moment? This is one of the least understood things about the tech industry. We have this society-level question that is not being addressed directly. It's being addressed by misunderstood proxy questions.

Taking as written that the finance industry is a branch of government in a meaningful sense, should the tech industry also be a branch of government? We don't ask that question directly. We have asked instead things like, “should the tech industry be responsible for minimizing the spread of misinformation?”

There was an injunction issued in a court case last year on the 4th of July, which I find oddly aesthetically motivating. The court case is _[Missouri v. Biden](https://en.wikipedia.org/wiki/Murthy_v._Missouri)_. The argument made in the court case — which the judge accepted and is extremely well supported by the record in front of him — is that various actors within the United States government puppeteered the tech companies and used them as [cat's paws](https://en.wikipedia.org/wiki/Cat%27s_paw_theory) to do frankly shocking violations of constitutionally protected freedoms such as the freedom of speech.

It wasn’t on the level of "we've built this unaccountable, hard-to-inspect system of LLMs and heuristics and we started turning off a lot of people's feeds on Facebook." But there was an individual person in the White House who was sending out emails like, "when are you going to address me on this tweet, guys? We can't have things like this anymore."

Again, it’s a feature of the United States that we are very good about keeping records and transparency and having a functioning legal system. I was following along as this was happening. What was happening was much worse than what I understood to be happening.

Here’s an example of something that, as we were growing up as children, you would never think that the United States federal government would do. I believe it was the state of Missouri. They said "hey, you have town halls where citizens can come in and speak their mind and advocate for their policy preferences. You probably have a civics class and talk about the [First Amendment](https://en.wikipedia.org/wiki/First_Amendment_to_the_United_States_Constitution) and things. Yeah, someone said something we don't like in a particular town hall. Take down the recording from YouTube."

That happened. That is a violation of the constitution of the United States. That is against everything in the traditions and laws and culture of the United States. That is outrageous. Yet it happened. We have not repudiated the notion of using tech as cat's paws.

This is literally written in the [decision](https://www.supremecourt.gov/opinions/23pdf/23-411_3dq3.pdf), which I would urge everyone to read by the way. There was an individual in a non-governmental organization which was collaborating with the governmental organizations in doing this. They said something like, "to get around legal uncertainty, including very real First Amendment concerns, in our ability to do this, rather than doing it in the government directly, we are outsourcing it to a bunch of college students who we have hired under the auspices of this program."

What? One, just as a dangerous professional, you have violated _[The Wire](https://en.wikipedia.org/wiki/The_Wire)_[’s](https://en.wikipedia.org/wiki/The_Wire) [Stringer Bell's dictum](https://youtu.be/pBdGOrcUEg8) on the wisdom of taking notes on a criminal conspiracy. You literally wrote that down in an email! The outrageous part is not that you wrote that down in an email.

The outrageous part is that you — with full knowledge of it — engaged in something that is outrageously unconstitutional, immoral, illegal, and evil, to the applause of people in your social circle. Everyone involved in the story thinks that they're the good guy in it. If you write that email, you are not the good guy in the story.

**Dwarkesh Patel** _01:17:04_

What is your sense of what the judicial end result on this will be?

**Patrick McKenzie** _01:17:15_

I think there will be a limited hangout and walkback of some particular things. There does exist an injunction. I would predict that continues to happen in the future. What do I know? I'm just a software guy.

Do people want to achieve power? The tech industry has power because it is good at achieving results in the physical world. This is certainly not going to be the last time that someone desiring power thinks, "can I force you to give me the power that you have accumulated?" That is fundamentally a political decision about how we construct our democracy. We should make good decisions about that.

**Dwarkesh Patel** _01:18:02_

Maybe that's the crux here. Your story of VaccinateCA illustrates the lack of accountability in our institutions. It seems fanciful that we can go back to Congress and pass some law. We have KYC/AML. We realized that with LLMs, it's going to be a bad deal with regards to privacy. We're going to roll that back. We don't like the collusion between tech and whoever's in power. We don’t like this ability to dictate what can get taken off the platform. We think that's free speech and we're going to pass laws and take that back.

There's no sense in which society has come to a consensus about the privacy and free speech concerns we have. By at least one argument, the solution is that you just start new rails for these things that cannot be constrained in this way. It's not a matter of just changing the KYC law. Rather, that's implausible given the manifest declining state capacity we've talked about.

**Patrick McKenzie** _01:18:59_

I don't accept that it is the only thing possible for us. I don't accept that the United States is incapable of doing nice things. We can't accept that. We have to be optimistic about the future. Otherwise, what are we doing here?

In the tech industry, we know it is not a physical law of reality or of large institutions that one cannot make systems that work. Making systems that work is the job. We have a few existence proofs. We should increase our engagement with government. Hey state capacity, we can help you build some of that stuff. Also, the Constitution of the United States is a document we feel attached to.

Again, incentives rule everything around us. In early 2021, the tech industry was very concerned about being told in no uncertain way by people in power, "if you embarrass us, we'll end you." One thing in the judicial record of this case is that the White House and other government actors routinely overreached and asked the tech companies, "we would like you to censor this and this and this." The tech companies said no in a bunch of cases.

It’s important to continue to negotiate for the right outcome rather than the one that people in power merely want. There are some things that will feel unfortunate and maybe a little bit outside of our true sweet spot of what we would want to be doing on a Tuesday in tech. Maybe we have to ratchet up the amount of public policy advocacy that we do. Lobbying is a dirty word in the tech industry. It probably shouldn't be.

When the "do not embarrass us" order came down, people were getting very quiet about the fact of feeling constrained by this. Maybe we should have spoken out more and spoken more boldly about it. It was the routine case that the White House was telling Facebook, Twitter, etc. to censor on a tweet by tweet, communication by communication basis.

This is also with regards to broad rules that affected the residents of the United States and also everyone else in the world. These are the operating systems of the world. They were giving direct orders on, "there's a certain kind of speech act which we find vexatious and we would like you to stop that everywhere." Very plausibly, we should get on the nightly news and say, "I received the following email from the White House that says we should stop this everywhere.” If you point a gun at me, I will comply with this at the point of a gun. That is what it will take.

**Dwarkesh Patel** _01:21:55_

It almost requires civil disobedience.

Say you’re right that in 2021, there were going to be serious political repercussions on the tech companies. Say they publish this email, “here's what the White House just sent me to take down this tweet.” Now, Twitter's market cap has just collapsed because people realize the political implications of what Jack Dorsey just got up and said at the time.

Then the solution is that you need tech companies to basically sacrifice their capacity to do business. Maybe that is a solution, but that's not a story about optimism about the ability of the US government to solve problems this way.

**Patrick McKenzie** _01:22:37_

You need to have a risk tolerance, right? Every business everywhere, including the financial industry and the tech industry, is balancing various risks. The risk tolerance was poorly calibrated.

One can achieve results in the world by doing things like embarrassing government officials. Embarrassing a person in a position of authority is not a zero risk behavior. It is relatively low risk in the United States relative to other places.

That was extremely important for VaccinateCA. People thought at the beginning, are we going to get in trouble for publishing true information about vaccine availability that will embarrass the state of California? I said, “I have a very high confidence that no matter what we do vis-a-vis the state of California, that you cannot get in serious trouble in the United States for saying true things.” The First Amendment exists. We have backstopping infrastructure here. If push comes to shove, we will shove back and we will win.

This is just me as a guy who took the same civics course that everyone took and does not have a huge amount of resources relative to the entire tech industry. Maybe we need to have a certain amount of intestinal fortitude. Okay, you've asked us to do something, you've threatened us with taking away all the wonderful toys and the great business models that make this an extremely lucrative area to work in. You’ve asked us to sacrifice a value that is very important for us to continue to do that. No, we're going to fight you on this one.

The comms-trained part of me is saying, "don't use the word fight." We are going to collaborate with stakeholders across civil society to achieve an optimal outcome, balancing the multiple disparate and legitimate interests of various arms of the government and civil society and blah, blah, blah. Sometimes that requires fighting. We should fight when it does.

**Dwarkesh Patel** _01:24:36_

[On Tyler's podcast](https://conversationswithtyler.com/episodes/patrick-mckenzie/), you said something like, “America doesn't have the will to have nice things and Japan does.”

**Patrick McKenzie** _01:24:44_

In some ways, yes.

**Dwarkesh Patel** _01:24:45_

I’m thinking about your own [essay about working as a salaryman](https://www.kalzumeus.com/2014/11/07/doing-business-in-japan/). You're working 70-hour weeks. You're killing yourself to get that marginal adornment on the products you're making.

Isn't it better that we have a system where we put in 20% of the work to get 80% of the results? We spend the rest of the effort on expanding the [production-possibility frontier](https://en.wikipedia.org/wiki/Production%E2%80%93possibility_frontier). It's good that we don't have the will to have nice things. We just get it done.

**Patrick McKenzie** _01:25:13_

I don't think these trade off against each other at the relevant margins. Nothing about culture is monocausal. I also don't think culture is a sufficient explanation for some of the differences that are achieved in the United States vs. Japan.

There's a great book, _[Making Common Sense of Japan](https://amzn.to/3We6L3r)_. The author makes this persuasive argument at length. I don't think it’s 100% true, but it's more true than most well-informed people on either side of the Pacific believe.

He argues that when people say, "they do this because it is Japanese culture," what they're often saying is this. I usually have an incentive-driven model for why people do things. I understand this incentive. Then there's some error term in this equation that I don't understand. I'm going to call that error term, "culture." To be clear, culture is a real thing in the world. But we reach for that error term far faster than we should.

There are places in pockets of the United States that have the will to have nice things. Often they discover that surprisingly the only thing you need is to choose to have nice things. You don’t necessarily have to spend more money. People don’t have to kill themselves with 90-hour weeks for the entirety of their career. You can just choose to have nice things. Let's choose to have nice things. Let's not be embarrassed about choosing to have nice things.

**Dwarkesh Patel** _01:26:41_

You understand all this financial plumbing. If you were an investigative reporter, what is the thing you're looking at that the average newspaper reporter wouldn't know to look at to investigate a person or a company or a government institution?

**Patrick McKenzie** _01:26:56_

I have an enthusiasm for the minutiae of banking procedure in a way that few people do. Sometimes banking procedure causes physically observable facts to emanate into the world. If you know that those facts are going to emanate, then you can have a claim made about a past state of the world. I did this thing. I did not do this thing. If true, that claim will cause metadata in other places and you can look for the metadata.

This is actually how a lot of frauds are discovered. Basically the definition of fraud is that you're telling someone a story. The story alleges a fact about the world. The story is not true and you're using the story to extract value from them. Most frauds will allege facts about the physical world.

As the physical world gets more and more mediated by computers, it gets increasingly [sharded](https://en.wikipedia.org/wiki/Shard_/(database_architecture/)) between different institutions. There will often be institutions that are not under control of the fraudster and have information available to them, which will very dispositively answer the question of whether the alleged fact happened or not.

As a reporter, it’s important to understand how institutions and society interact with each other. It’s important to understand the physical reality of how if this thing happens as alleged, then these papers will be filed, then these API calls will be made, etc. Then doing the core job of reporting involves finding people at the institutions who will tell you the truth.

As an example of this, many years ago [Mt. Gox](https://en.wikipedia.org/wiki/Mt._Gox) was [insolvent](https://en.wikipedia.org/wiki/Insolvency). That fact was widely rumored but not reported, presumably because the global financial news industry didn't find it convenient to have someone call into the Japanese banking system and ask the right questions in the right way. The CEO of Mt. Gox alleged on [BitcoinTalk](https://bitcointalk.org/) that the reason they were not able to make outgoing wires was because they had caused a [distributed denial of service attack](https://en.wikipedia.org/wiki/Denial-of-service_attack) on their bank's ability to send foreign currency wires.

That bank was [Mizuho](https://en.wikipedia.org/wiki/Mizuho_Bank). Mizuho was the second largest bank in Japan. Many people at well-regarded financial reporting institutions in New York City find it incredibly exotic and difficult — and maybe in some ways unknowable — to extract facts from Mizuho.

There are addresses. FedEx will deliver letters to them. They have phone lines. We also have fax machines. We love our fax machines. Could you send a fax to anybody at Mizuho and say, "hey, quick question, are you sending wires today?" Mizuho would receive the fax, look at it quizzically, and say, "in response to your fax earlier, yes, we are still sending wires because we are the second largest bank in Japan. Do you have any other easy to answer questions for us?"

Financial reporting dropped the ball on asking Mizuho simple questions about reality. Maybe you should do that next time. The CEO is giving out gold on BitcoinTalk under his own name. These are obviously reportable statements. The statements are alleged facts about material reality. Maybe chase down the truth value of that.

That's hard. It's so much easier to just repeat what he says on Twitter and say, "as said by this person on Twitter," and then quote the Bitcoin price feed. But reporting is hard. Be good at it.

**Dwarkesh Patel** _01:30:40_

Why aren't [short sellers](https://en.wikipedia.org/wiki/Short_/(finance/)) doing this? They should have an economic incentive to dig to the bottom of this, right? We should have a deluge of financial information from short sellers who call the banks and trace through the API calls.

**Patrick McKenzie** _01:30:51_

That is an ongoing interesting question. Short sellers provide an enormous service for the world in being essentially society's best sleuths on financial fraud. Yet they fail to detect lots of them. I’m not just throwing short sellers or reporters or anybody else under the bus.

I failed to detect [SBF](https://en.wikipedia.org/wiki/Sam_Bankman-Fried)’s various craziness, despite having sufficient information available to me as a well-read person on the internet to have detected that. Where were the freaking wallets? Essentially, everybody assumed someone else was looking at it.

That's one reason. Short sellers often assume they need to first get put on the path of something and have a differentiated point of view. Another issue for short sellers is they have to find an instrument and they have to find another side of the trade to successfully do that. Without being expert on Bitcoin micro mechanics, I’ll say it was difficult to make the trade in size. Mt. Gox was insolvent. You could try to pull money out of Mt. Gox, which people were definitely trying to do.

I got a number of interesting business proposals from people around 2012. They said, "hey, you're an American and you clearly understand international banking and you live in Japan. Could I have you get some yen and wire that to me in America and you can take a percentage?" I really don't like where this is going.

They said, "there's this company and I've got some money over there. They can send yen, but they can't send dollars."  Is that because they don't actually have the money? They're like, "no, it's a Japanese banking thing." Okay, no it's not. Japanese banks are very good at sending wires. They said, "no, it's really this thing. This is totally clean.

You would not be having this conversation with me if it was totally clean. You need a money launderer. I will not be your money launderer.

**Dwarkesh Patel** _01:32:47_

How hard is money laundering? You mentioned earlier that banks have the capacity where every transaction is analyzed and flagged. If it's notable enough, they write a report about it. How sophisticated does the cartel need to be in order to move around, say seven-figure amounts of money?

**Patrick McKenzie** _01:33:10_

The definition of money laundering is extremely stretchy. There's a spectrum of people. Much like there's a spectrum of sophistication in financial fraud, there's a spectrum of sophistication in money laundering. If you want to look at probably the most sophisticated money launderer in history, he’s currently a guest of the US government, wherever SBF is staying.

**Dwarkesh Patel** _01:33:32_

He was sophisticated?

**Patrick McKenzie** _01:33:33_

This is a disagreement I have with a lot of people. SBF was extremely sophisticated. It's not just SBF. People identify him uniquely. They identify the inner circle uniquely as being at fault here. There was an entire power structure there, which was extremely adept at figuring out how power worked in the United States and exercising it towards their own ends.

Then it blew up. Until then, my goodness. They decided we need regulatory licenses. They're called [money transmission licenses](https://en.wikipedia.org/wiki/Money_transmitter) in the United States. Those are done on a state-by-state basis. They got 50 regulators to sign off on it, etc. There were many objective indicia of them being very good at their jobs until they lost all the money.

**Dwarkesh Patel** _01:34:20_

Wasn’t it more about getting people to look the other way politically rather than figuring out how to structure the wire in a way that won't get flagged?

**Patrick McKenzie** _01:34:28_

It's not merely a matter of getting them to look the other way. Go back to the original [SBF interviews](https://www.bloomberg.com/news/articles/2021-04-01/the-ex-jane-street-trader-who-s-building-a-multi-billion-crypto-empire) where he's telling the founding myth of [Alameda](https://en.wikipedia.org/wiki/Alameda_Research). He says very loudly that the reason why he got this opportunity to do bitcoin [arbitrage](https://www.investopedia.com/terms/a/arbitrage.asp) between Japan and the United States is because he was [able to do something that the rest of the world wasn't](https://protos.com/bankman-fried-curliest-crypto-billionaire-etfs-bitcoin-japan/).

He doesn't say this in these many words. I will say it. He suborned a Japanese bank. You need that as one of the pieces to run this arb and then he pulled tens of millions of dollars out of this. I don't think people really listened to what he was saying there. He literally says in [the interview on](https://www.bloomberg.com/news/articles/2021-04-01/the-ex-jane-street-trader-who-s-building-a-multi-billion-crypto-empire) _[Bloomberg](https://www.bloomberg.com/news/articles/2021-04-01/the-ex-jane-street-trader-who-s-building-a-multi-billion-crypto-empire)_, "if I was a compliance person, this would look like the sketchiest thing in the world. This looks like it's obviously money laundering." Because it is money laundering.

Interestingly, Michael Lewis [retells the story](https://amzn.to/4dbfqdM) and locates the story in South Korea rather than in Japan. Some people who were involved say they tried it in South Korea and Japan. I wish people would pull on more threads there. There's still lots of that story that we don't know.

Anyhow, how sophisticated do you have to be to launder tens of billions of dollars? SBF did that. That is a bar for sophistication. He was eventually caught. He was not caught for laundering tens of billions of dollars. He wasn't even under suspicion for laundering tens of billions of dollars around.

SBF was [Tether](https://en.wikipedia.org/wiki/Tether_/(cryptocurrency/))'s banker. Alameda Research — one of the parts of the corporate shell game they were playing — moved tens of billions of dollars of cash around the financial system. It did so largely under full color of law on behalf of Tether. It moved it from wherever Tether or their customers had it to, at the moment, I think [it's mostly at Cantor Fitzgerald](https://www.bloomberg.com/news/articles/2024-01-16/tether-s-custodian-says-the-crypto-giant-has-the-money-it-claims). Some shoe has to drop there eventually. I will eat a lot of popcorn when it does.

Be that as it may. There's many other ways to launder money. Let's say I establish a shell corporation and I buy a piece of real estate in New York City. I rent that real estate out to people. I collect a stream of rents from that. That money looks clean because there is an excellent business. It's my shell corporation that is renting this real estate that really exists, to a totally legitimate person. This money is clean.

The money that I put into the system to buy this on behalf of the shell corporation, I'm just going to wire it to a lawyer. The lawyer is going to answer any question from the bank with, "I don't know where it came from. I don't have to tell you. I'm a lawyer. It's a real estate transaction. What do you want from me?"

In one sense, that's money laundering if the original money was the proceeds of crime. In another sense, that's how every real estate transaction goes down at those scales. Often a facility at money laundering is just a facility at operating the economy, plus willingness to do that to hide the proceeds of some other crime.

I would be really good at money laundering. I'm glad I haven't done it professionally. It's fascinating intellectually. Previous communications departments I've worked at probably explicitly anti-endorse that sentiment. What can one do?

**Dwarkesh Patel** _01:37:36_

We are reasonably confident that you're not laundering money.

**Patrick McKenzie** _01:37:39_

I would be much wealthier if I was.

**Dwarkesh Patel** _01:37:42_

This is a separate topic. You emphasize that people tend to undercharge for the products they serve. Let’s say you have identified somebody who actually does charge for products what they can get away with.

Psychologically, what do they have that the rest of us don't?

**Patrick McKenzie** _01:37:57_

Interestingly, this is one of those places where culture is not merely a term but actually descriptive in some ways. It gets contentious so I don’t want to point fingers at particular examples. There are some cultures in the world that have institutionally adopted more of a pro-capitalist, pro-mercantilist ethos. They have less of an ingrained skepticism regarding earning money and accumulating resources as a goal.

There are other cultures which have an extremely ingrained skepticism about earning money and accumulating resources as a plausible goal. Those cultures generate people who have very different negotiation strategies. When you impact people with different negotiation strategies against the reality of a well-operated organization like Google for example, they arrive at very different numbers.

Is it [Amy Chua](https://en.wikipedia.org/wiki/Amy_Chua) who wrote [a book about “market-dominant minorities?"](https://amzn.to/4dcVHKN) All people are equal in the eyes of God and hopefully in the eyes of the law. Not all cultures physically make the same decisions with regards to the same facts on the ground. That causes some disparity in outcomes. That is one tiny part of that thesis. I've read a lot of books. I don't necessarily endorse every word in every book that I read. However, there is something to that.

Another thing is that there's a certain personality-type cluster of people that got into tech. It is over-advanced that the tech industry and the pathologies of the tech industry are caused by the [nerd vs. jock distinction](https://en.wikipedia.org/wiki/Nerd#Stereotype) in American high schools, heavily over-advanced. What’s the amount of truth to that? Not zero. Many of us came up feeling we were largely getting beaten down by the system around us. We were not worthy, etc. Then we carry those issues into our professional lives. Some people work their way out of it quickly. Some do not.

For class and other reasons, some people go to institutions like Stanford and hear from… I don't know who you hear things from if you go to Stanford. I certainly didn't go there. Let’s say it’s an elder fraternity brother that says, "yo bro, this is the way the world works. You really got to negotiate when you get an offer in your discussion with Google. I've talked to so many brothers and they don't negotiate. The ones that do make a whole lot more money." You're like, “wow, good for that." Most people don't get that talk from their elder fraternity brother because they do not go to Stanford and don't have an elder fraternity brother.

Until VaccinateCA, the most important thing I'd probably done professionally was writing [a piece on the internet about salary negotiation](https://www.kalzumeus.com/2012/01/23/salary-negotiation/). It's subtitled, "Make More Money, Be More Valued." It’s an exhortation for mostly young people who had some of the issues I had when I was young and growing up. You're allowed to negotiate. That's not a moral failing. You have no less right to the marginal dollar than a company has to the marginal dollar. Go get it. Then you can put it towards all sorts of interesting ends.

500,000 people a year read that piece and it's now 12 plus years old. I keep a folder in Gmail about who has written and said “I got $25,000 to $100,000 per year more as a result of reading this piece.” I used to keep a spreadsheet. I stopped keeping the spreadsheet after it had ticked into the eight figures and it became an ongoing source of stress for me.

**Dwarkesh Patel** _01:41:40_

Eight figures?

**Patrick McKenzie** _01:41:41_

Yeah, per year. You would assume that 500,000 people read it per year. Some take the advice. Most who take the advice probably don't write me to say, "hey, I took the advice, thank you." Maybe I missed some emails. The true economic impact is probably larger than that.

There are probably people who have the inverse of that spreadsheet where it's like, "darn it. We got quoted [@patio11](https://x.com/patio11) against us again.” We’ve got these numbers and there's only a few firms in the tech industry that do scaled hiring.

**Dwarkesh Patel** _01:42:14_

There seem to be fewer people in their twenties who have prominent software businesses today than maybe 10 to 20 years ago. You’ve been in the software industry over a long period.

Is it because the nature of software businesses has changed or is it because the 20 year olds today are just less good?

**Patrick McKenzie** _01:42:39_

I've met many young and talented people over the course of 20 years in the software industry. Young and talented people continue being young and talented. One partial explanation is that when there's a new frontier that opens up, the existing incumbents — institutions and people with deep professional networks and personal resources — do not immediately grab all the value in that new thing. It's terra nova.

To the extent that tech is no longer terra nova, you would expect fewer people who are less resourced and younger to rise to the heights of prominence in tech. To be clear, I'm not at the heights of prominence in tech. When I ran companies, I was not running companies like some [other guests on this podcast](https://www.dwarkeshpatel.com/podcast) run companies. It was a [bingo card creator](https://training.kalzumeus.com/newsletters/archive/selling_software_business). I was making bingo cards for elementary school teachers while living next to a rice paddy in central Japan.

That's my dominant hypothesis. There are some things that are affecting the youth that I think are negative. Some products that the tech industry has created do not maximize for the happiness or productivity of people that consume those products: TikTok, etc.

I continue to be bullish about the youth. I have two children who, knock on wood, will accomplish things in their lives. I'm intrinsically skeptical about, "oh, the kids these days, they're just bad kids."

**Dwarkesh Patel** _01:44:02_

How much do you worry about video games as a sort of [wireheading](https://en.wikipedia.org/wiki/Wirehead_/(science_fiction/)). Somebody like you were 20-30 years ago, now has access to _[Factorio](https://www.factorio.com/)_. Will they just wirehead themselves to that instead of making a really cool software product? How much should we see this in the productivity numbers?

**Patrick McKenzie** _01:44:23_

Oh, goodness. I don't know about the productivity numbers. Generally, I do know that Steam keeps a counter of how much I'm playing video games in a year. Knock on wood, I've accomplished a few things in my career. Against that, what was my Steam counter up to?

Steam didn't include _World of Warcraft_. _World of Warcraft_ was at least 1000 hours for me. Factorio recently was 750. If you sum it all over 20 years, I've probably played video games for 4,000-6,000 hours. That's two to three years of professional effort, if one thinks that it trades off directly with professional effort.

**Dwarkesh Patel** _01:45:02_

Do you? Include every single young guy who's a nerd. How much are we worried that a bunch of their productive time is going to video games instead of making the next software business?

**Patrick McKenzie** _01:45:17_

I worry at least a little bit about it for myself. I recently started working with an executive assistant. One of the first suggestions that he gave was, "hey Patrick, will you friend me on Steam so that I can see how much you're playing any given week? That way if you're not making your priorities happen, we can have an honest discussion about priorities."

That's really good advice, given that I spent far too much time ratholing on _Factorio_ relative to my true preferences.

**Dwarkesh Patel** _01:45:42_

You've got a really confident [EA](https://en.wikipedia.org/wiki/Secretary#Executive_assistant).

**Patrick McKenzie** _01:45:45_

Go, Sammy, go.

**Dwarkesh Patel** _01:45:49_

Hey boss, can we have an honest conversation tonight?

**Patrick McKenzie** _01:45:52_

I don't know if I'm inserting those words into his mouth.

The suggestion was genuinely his. On the one hand, _Factorio_ is a wonderful game. I actually think Factorio matters far more to the world than most video games do. That's an entirely different piece that I'm trying to write at the moment.

**Dwarkesh Patel** _01:46:06_

Have you read [Byrne's piece on this](https://www.thediff.co/archive/the-factorio-mindset/)? “The _Factorio_ Mindset”

**Patrick McKenzie** _01:46:09_

Yes. I love many things Byrne writes. I think I luckily have a differentiated point of view on this one. I hope to get it out to the internet someday.

On the one hand I loved it. The _Factorio_ [space exploration mod](https://mods.factorio.com/mod/space-exploration) specifically was the best video game I ever played. Yet I spent 750 hours on that over the course of a year. I was on sabbatical and recharging from six very hard charging years at Stripe and also running the United States vaccine location information effort. But there's a question of, at relevant margins are you maximizing for your true values? I was a little worried about that. Now my EA checks on me. Do I worry about it for other people?

When I was young and a _World of Warcraft_ [raid](https://wowpedia.fandom.com/wiki/Raid) guild leader who spent a thousand hours on that, it was a substitute advancement ladder for me. The actual job I was working, selling around central Japan, gave me no scope of control over things. I thought if I were a startup CEO, I could make decisions right now. I could build something awesome, but I don't have that ability. I don't see myself as being the kind of person who could become a startup CEO.

If I can't be satisfied with my nine-to-five job in terms of making things happen in the world, at the very least I can do this. Make sure we kill the dragon in two hours. Guys, don't stand in the fire. Come on, team leaders, you need to make sure that people are equipped with the resist gear before they get there. We're having internal spats about allocation of resources. We need to have a better [DKP](https://en.wikipedia.org/wiki/Dragon_kill_points) system.

By the way, World of Warcraft raid guilds — and all other places where intellectual effort comes together in the video game community — are much more sophisticated than people give them credit for. When I started VaccinateCA, I told people my sole prior leadership experience was having 60 direct reports in a raid guild. That's true. I don't want to rat hole on the subject, but there are parts of VaccinateCA that are very definitely downstream of the intellectual efforts involved in managing raid guilds specifically. There were multiple people internally who were like, “yep, we are running the raid guild playbook right now.”

Be that as it may, you can do something with your life. Choose to do something with your life. Then if you want to play a reasonable amount of video games, then play a reasonable amount of video games.

With respect to individual people, I've struggled with depression at some points in my life. Many people struggle with under-diagnosed, under-treated depression. Sometimes you get into a self-destructive spiral measured against your true values and preferences. Due to depression and other factors, you aren't making as much progress on the true goals. You use video games as an escape from that. It’s not just video games but books, television, etc.

There are many poisons available. You pick your poison and use that to escape. The amount of effort you put into the poison causes you to have less effort available to do the true thing. So you get worse results at the true thing.

Helping people out of those self-destructive spirals is something that we as a society could stand to get much better at.

**Dwarkesh Patel** _01:49:28_

Speaking of Byrne, I noticed that many of my favorite writers are finance writers. There's you, Byrne, [Matt Levine](https://www.bloomberg.com/opinion/authors/ARbTQlRLRjE/matthew-s-levine). Is there a reason why finance has attracted so much writing talent?

**Patrick McKenzie** _01:49:42_

There are many good writers in the world, [Derek Thompson](https://www.theatlantic.com/author/derek-thompson/) for example. He's a chemical engineer and has written about some things I can barely understand. I have enough of an engineering degree where I can appreciate half of the chemistry but I can’t appreciate the full totality of why, for instance, [uranium hexafluoride](https://en.wikipedia.org/wiki/Uranium_hexafluoride) is such a terrible substance to work with. He has some excellent writing on why that’s a terrible substance to work with.

**Dwarkesh Patel** _01:50:01_

The broader question is, why does finance have a greater concentration of writing talent? Not just for current bloggers, but finance histories are some of the best history books out there. I’m thinking of those by [Bethany McLean](https://amzn.to/4fjzmwP) and so forth.

Is it an intrinsically more interesting subject, or is there some other reason?

**Patrick McKenzie** _01:50:22_

There’s some path dependence. If I had ended up working in a water treatment plant, I'd probably be writing about water treatment plants because I enjoy writing. I know enough about myself to say that a discussion about how [alum works in water treatment plant](https://www.ninemilecreek.org/wp-content/uploads/Alum-Education_2019.pdf) — something I read about when I was six — could captivate me for years. I'd write about it if I was captivated by it.

I agree with a point Matt Levine made once. Finance and the tech industry have for a while been relatively reliable ways to turn intelligence into money. Many good writers are very intelligent. Not all intelligent people are good writers. It's a skill that more intelligent people could learn. If we create an incentive system that tends to allocate many of the country's top minds into specific fields where they become experts, I'd expect a lot of writing talent to emerge there as well. Good writing is good thinking. That's a [Paul Graham quote](https://paulgraham.com/read.html) I believe, and it's broadly true.

**Dwarkesh Patel** _01:51:26_

If I remember correctly, you went to Japan because you thought that after the dot-com boom, the demand for programmers alone would diminish and a combination of skills would be required. You weren't the only one who thought this way.

**Patrick McKenzie** _01:51:45_

Yes, and _The_ _Wall Street Journal_ said the same thing. _The Wall Street Journal_ had never been wrong in my experience as a 19-year-old who knew nothing about anything.

**Dwarkesh Patel** _01:51:49_

Separate from the object-level predictions you might have gotten wrong about the software industry, what was a meta-level mistake you made? How would we characterize that?

**Patrick McKenzie** _01:52:03_

I had a lot of rigor chasing a decision that had no basis in fact. I believed _The Wall Street Journal_ when it said that all future engineers would be hired in places like India and China and not the United States. The implication was that there would be no future engineering employment in the U.S.

I made a spreadsheet with the languages my university taught, my best estimate of the number of Americans who spoke them, the amount of their software sold here, the amount of US software sold there, and so on. I multiplied these together and sorted by column H, descending. This was [LARPing](https://en.wikipedia.org/wiki/Live_action_role-playing_game) rigor, but it felt like a good decision-making process at the time. The meta discussion is: don't LARP having rigor. Actually have rigor.

**Dwarkesh Patel** _01:52:47_

But what would that look like in this context? What would you have done differently?

**Patrick McKenzie** _01:52:51_

Ultimately, I'm happy with the decision I made although it might seem like the wrong decision. I’m happy because of other life factors. Working in Japan as a young engineer had some very rough parts. But on a mental level, this was an early opportunity to trust institutions less and trust systemically viable reasoning patterns more.

Assuming I’m remembering this article correctly — and it was a pivotal moment for me — _The Wall Street Journal_ asserted that no future Americans would be hired at software companies. Assume this is true. What happens in the American software industry? Maybe I didn’t have enough knowledge to confidently predict that at the time.

But I can confidently predict some things now. For example, software companies are going to break as older engineers age out and no one is coming up to replace them. The industry must hire people every year. Hiring freezes are necessarily temporary as a result of that. That’s as close to a law of physics as one can have. If you tell me something which says the laws of physics have been suspended and will be in the future, I won't agree with that.

How would I learn the law of physics? I didn’t know anyone in software engineering at the time, which is partly why I was getting my advice from _The Wall Street Journal_.  I was at a research university in the US. If I had been slightly more agentic about it, I could have found someone who knew someone in the software industry to explain this to me.

**Dwarkesh Patel** _01:54:28_

Couldn't you use that same logic to say that journalism jobs won't go down because senior journalists will have to be replaced by new journalists? It’s true, but it doesn't take that many people to study journalism. It actually would have been a bad call to major in journalism and pursue that as a career.

**Patrick McKenzie** _01:54:43_

The fundamental thesis for journalism is that the total size of the pie is decreasing due to structural factors. _The Wall Street Journal_'s thesis wasn't simply that the size of the pie would decrease in the wake of the dot-com bust, but more so that companies will maximize for labor costs and therefore ship out all the jobs.

**Dwarkesh Patel** _01:55:08_

I see. You've emphasized that founders should do more [A/B testing](https://en.wikipedia.org/wiki/A/B_testing). That's a main theme of your blog. They should do this because they under-optimize on it.

What do they tend to over-optimize on?

**Patrick McKenzie** _01:55:24_

Interestingly, I was a marketing engineer earlier in my career and really thought that was important. In terms of high-level advice, I'd probably tell a founder a bit about marketing engineering. I wouldn't spend 95% of my time on it unless that was explicitly why they brought me in.

What do founders spend too much time on? Playing house and chasing status are two well-known pitfalls. Your incentives will draw you into playing the role of a successful CEO before your actions have earned the company its level of success. The fundamental nature of early-stage businesses is that investment in you is not an indication of what you have achieved. It’s an advance on your future accomplishments. You need to rigorously pursue actually making those future accomplishments.

There are many ways to pursue this. Talk to more users, write more software, make something excellent, get more people to use it, get better at selling it, etc. This is an important strain of Silicon Valley culture. I'm glad we have it and we're popularizing it worldwide, including to me in central Japan.

Yet there are always other games going on. Those games are less important but very attractive. Not video games, but things like attending conferences, meeting interesting people, or going to the best parties. Showing up at the best parties does not, at most margins, increase the number of users you talk to. It doesn't write functioning code. Do the things that actually matter. Some distractions proudly wave, "I'm a distraction from everything that matters." Some don’t. Others feel like real work but are not. Don't do the things that don't matter. It sounds vacuous and yet…

**Dwarkesh Patel** _01:57:30_

Let’s go back to VaccinateCA and close the loop on a question. I don't think we got a good answer but I think it’s important.

Suppose you're the president of the United States, a new one replacing the current one. Looking back on what happened, if you were president, what would you do to create accountability and ensure we’re ready for a future crisis? Maybe you fire the right people, but beyond that, there’s a lot of different things that could go wrong. How do you make sure we're ready for them?

**Patrick McKenzie** _01:58:06_

One cultural practice of the tech industry that would be salubrious for broader civil society to adopt is the concept of [blameless postmortems](https://sre.google/sre-book/postmortem-culture/). We talked earlier about who to blame for various failures. I broadly believe that some amount of blame performs useful societal purposes. Beyond that, diminishing returns set in quickly.

The magic word in Washington is accountability. People want accountability for failures. Accountability terrifies people. This causes fields of distortions around what actually happened, mistakes made, and opportunities missed.

Changing our practice to achieve accountability in a more productive way involves first getting a dispassionate record of what actually happened. It’s less important to focus on which official was responsible or under which legislative authority. What did we do? How did our actions lead to the outcomes we got? Given those outcomes, what could we have done better? How do we inject that back into the system so that the next time this happens, we don’t repeat the mistakes?

Sometimes this will involve someone losing their job, though hopefully not often. A non-zero amount is important to note. There are many aspects we should postmortem about this experience, though we don't have several thousand hours to go over all of them.

There should be an inquiry. At a minimum, let's ask all involved parties to write down the history of the COVID experience dispassionately, recording dates, times, and actions taken. We want it to be truthful and comprehensive, highlighting the most important aspects. That is step one. Maybe we ask for step one, then move to step two.

**Dwarkesh Patel** _02:00:50_

Final question, what are you going to work on next?

**Patrick McKenzie** _02:01:00_

I don't exactly know what my next big professional splash-in will be. I've been on semi-sabbaticals here, writing _Bits about Money_ and being between 20-80% productive relative to my 100%. I might start a software company or raise a small VC fund. I might do something entirely different.

Currently, I’m focusing on family-oriented things. Our family immigrated from Japan to the United States and we're going through all the fun adjustment issues. I’ve focused heavily on my career over the past eight years. Now I’m rebalancing to help with this adjustment and then figure out what’s next for the next chapter of life.

**Dwarkesh Patel** _02:01:20_

Excellent. Patrick, thanks so much for coming on the podcast.

**Patrick McKenzie** _02:01:23_

Thanks very much for having me.