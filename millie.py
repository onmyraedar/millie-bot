import discord

from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
from discord.ext import commands
from splinter import Browser

token = open("TOKEN.txt", "r").readline()

description = "Hi, I'm Millie! I help artists combat art theft."

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)

embed_color = 0xe6c9ff

@bot.event
async def on_ready():
    DiscordComponents(bot) # Supports functional buttons
    print("Millie is ready for action!")

@bot.command()
async def info(ctx):
    """Provides the author with info about Millie."""
    info = discord.Embed(
        title="Hi, I'm Millie! I'm here to help artists combat art theft.",
        description="""
        As a digital artist, it can be incredibly frustrating when someone steals your work and tries to profit off of it.
        Thankfully, there's a law called the Digital Millenium Copyright Act (DMCA) that can help you get your stolen content removed.
        Many websites have __online forms__ for submitting your DMCA takedown notice.
        If such a form doesn't exist, you can __contact the site's DMCA agent directly__ or __reach out to the web host or ISP__.

        Type **!email** to learn more about DMCA takedown emails.
        Type **!contacts** to quickly access contact information for DMCA claims.
        Type **!forms** for help with DMCA forms for a particular site.
        """,
        color=embed_color
        )
    await ctx.send(embed=info)

@bot.command()
async def email(ctx):

    #Introduction

    intro = discord.Embed(
        title="Sending a DMCA email to a service provider is one way of getting your stolen content removed from their site.",
        description="""
        I'll ask you a few questions about the incident you'd like to report.
        Then I'll generate an email that you can send to a service provider.

        Is that okay? Click **Next** to proceed.
        """,
        color=embed_color
    )
    intro_next_btn = Button(style=ButtonStyle.blue, label="Next", custom_id="intro_next_btn")
    await ctx.send(embed=intro, components=[intro_next_btn])
    
    intro_interaction = await bot.wait_for(
        "button_click", check=lambda btn: btn.custom_id == "intro_next_btn"
    )

    await intro_interaction.send(content="Let's begin!")
    
    #Step 1: Describe your content

    step_1 = discord.Embed(
        title="Step 1: Describe your content",
        description="""
        Provide a description of the content that is being infringed upon.

        *__Example:__ a digital painting of a young lady sitting down at a table, wearing a lavender shirt and headphones, with her laptop open in front of her...*
        """,
        color=embed_color
    )    

    await ctx.send(embed=step_1)

    step_1_interaction = await bot.wait_for(
        "message", check=lambda msg: msg.author == ctx.author
    )

    # Step 2: Original links

    step_2 = discord.Embed(
        title="Step 2: Original links to your content",
        description="""
        Please provide the link(s) where *you*, the creator, originally posted your content.
        """,
        color=embed_color
    )   

    await ctx.send(embed=step_2)   

    step_2_interaction = await bot.wait_for(
        "message", check=lambda msg: msg.author == ctx.author
    )

    # Step 3: Location of the infringing content

    step_3 = discord.Embed(
        title="Step 3: Location of the infringing content",
        description="""
        Please provide the link(s) where *the infringing (stolen) copy of the content* is located.
        """,
        color=embed_color
    )   

    await ctx.send(embed=step_3)   

    step_3_interaction = await bot.wait_for(
        "message", check=lambda msg: msg.author == ctx.author
    )

    # Final step: Generate your email

    final_step = discord.Embed(
        title="Thank you!",
        description="""
        Click the button below to generate your DMCA takedown notice.

        Before you send the email to a DMCA agent, replace the fields in bold with your personal contact information.

        Use your **full legal name**, as the DMCA takedown notice is a legal action.
        """,
        color=embed_color        
    )
    email_btn = Button(style=ButtonStyle.green, label="📧 Generate DMCA Email", custom_id="email_btn")

    await ctx.send(embed=final_step,components=[email_btn])

    final_step_interaction = await bot.wait_for(
        "button_click", check=lambda i: i.custom_id == "email_btn"
    )

    content_description = step_1_interaction.content
    original_links = step_2_interaction.content
    infringing_links = step_3_interaction.content

    dmca_email = discord.Embed(
    title="Subject: Notice of Copyright Violation (DMCA Takedown Notice) - Request to Remove Offending Content",
    description=f"""
    
    To whom it may concern:
    
    My name is **[Replace with your full legal name]**. The following information is presented for the purposes of removing web content that infringes on my copyright per the Digital Millennium Copyright Act (“DMCA”). This notice constitutes an official notification under Section 512(c) of the DMCA.

    Under that statute, you are required, as a service provider, to remove or disable access to the infringing materials specified below upon receipt of this notice. Under the safe harbor provision of the DMCA, you are given immunity from liability for hosting the infringing content, provided that you quickly rectify and investigate the copyright infringement. Failure to do so can result in the loss of this statutory immunity.

    The content that is being infringed is {content_description}.

    The original content is located at the following URL(s):
    [{original_links}]({original_links})

    The infringing copy of this content is located at the following URL(s):
    [{infringing_links}]({infringing_links})

    I have a good faith belief that the use of the copyrighted materials described above on the allegedly infringing web pages is not authorized by the copyright owner, its agent or the law. Under penalty of perjury I certify that the information contained in this notification is both true and accurate, and that I am the owner of the copyrights involved.

    For further inquiry, I may be contacted as follows:
    **[Replace with your own email address or phone number]**

    Sincerely,
    **[Replace with your full legal name]**
        
    
    """,
    color=embed_color
    )

    await final_step_interaction.send(embed=dmca_email)

@bot.command()
async def contacts(ctx):
    contacts_dropdown = Select(
        placeholder="Choose one...",
        options=[
            SelectOption(label="OpenSea", value="OpenSea"),
            SelectOption(label="Tumblr", value="Tumblr"),
            SelectOption(label="DeviantArt", value="DeviantArt")
        ],
        custom_id="contacts_dropdown"
    )
    await ctx.send(
        "Select a site to view contact information for DMCA claims.",
        components=[contacts_dropdown]
    )

    contacts_interaction = await bot.wait_for(
        "select_option", check=lambda i: i.custom_id == "contacts_dropdown"
    )

    if contacts_interaction.values[0] == "OpenSea":
        opensea = discord.Embed(
            title="Contacting OpenSea about Copyright Infringement",
            description="""

            You can email your copyright request to __copyright@opensea.io__.

            You can also mail your request to the following address:

            Ozone Networks, Inc.
            Attn: Copyright Agent
            228 Park Ave S, #22014
            New York, NY 10003

            Note that only copyright owners and their legal representatives are eligible to submit a valid takedown request. OpenSea does not respond to takedown requests submitted by third party individuals.

            Source: [OpenSea Support Website](https://support.opensea.io/hc/en-us/articles/4412092785043-What-can-I-do-if-my-copyrighted-works-are-being-sold-without-my-permission-)
            """,
            color=embed_color            
        )
        await contacts_interaction.send(embed=opensea)
    elif contacts_interaction.values[0] == "Tumblr":
        tumblr = discord.Embed(
            title="Contacting Tumblr about Copyright Infringement",
            description="""

            You can email your copyright request to __dmca@tumblr.com__.

            You can also mail your request to the following address:

            Tumblr, Inc. (Automattic)
            60 29th Street #343
            San Francisco, CA 94110
            Attn: Copyright Agent

            Note that only copyright owners and their legal representatives are eligible to submit a valid takedown request.

            Source: [Tumblr Support Website](https://www.tumblr.com/policy/en/terms-of-service#dmca)
            """,
            color=embed_color            
        )        
        await contacts_interaction.send(embed=tumblr)
    elif contacts_interaction.values[0] == "DeviantArt":
        deviantart = discord.Embed(
            title="Contacting DeviantArt about Copyright Infringement",
            description="""

            You can email your copyright request to __violations@deviantart.com__.

            You can also mail your request to the following address:

            DMCA Complaints
            DeviantArt, Inc.
            attn. Daniel Sowers Jr
            7111 Santa Monica Blvd, Ste B, PO Box 230
            West Hollywood, CA 90046

            Note that only copyright owners and their legal representatives are eligible to submit a valid takedown request.

            Source: [DeviantArt Support Website](https://www.deviantart.com/about/policy/copyright/)
            """,
            color=embed_color            
        )        
        await contacts_interaction.send(embed=deviantart)        

@bot.command()
async def forms(ctx):

    #Introduction

    intro = discord.Embed(
        title="Many service providers have DMCA forms that can help you file a complaint easily.",
        description="""
        Please select your desired service provider from the dropdown below.
        Then I'll ask you a few questions to help you fill out their DMCA form.
        """,
        color=embed_color
    )
    forms_dropdown = Select(
        placeholder="Choose one...",
        options=[
            SelectOption(label="Tumblr", value="Tumblr"),
        ],
        custom_id="forms_dropdown"
    )
    await ctx.send(embed=intro, components=[forms_dropdown])

    forms_interaction = await bot.wait_for(
        "select_option", check=lambda i: i.custom_id == "forms_dropdown"
    )    

    await forms_interaction.send(content="Let's begin!")

    if forms_interaction.values[0] == "Tumblr":
    
        #Step 1: Describe your content

        step_1 = discord.Embed(
            title="Step 1: Describe your content",
            description="""
            Provide a description of the content that is being infringed upon.

            *__Example:__ a digital painting of a young lady sitting down at a table, wearing a lavender shirt and headphones, with her laptop open in front of her...*
            """,
            color=embed_color
        )    

        await ctx.send(embed=step_1)

        step_1_interaction = await bot.wait_for(
            "message", check=lambda msg: msg.author == ctx.author
        )

        # Step 2: Original links

        step_2 = discord.Embed(
            title="Step 2: Original links to your content",
            description="""
            Please provide the link(s) where *you*, the creator, originally posted your content.
            """,
            color=embed_color
        )   

        await ctx.send(embed=step_2)   

        step_2_interaction = await bot.wait_for(
            "message", check=lambda msg: msg.author == ctx.author
        )

        # Step 3: Location of the infringing content on Tumblr

        step_3 = discord.Embed(
            title="Step 3: Location of the infringing content on Tumblr",
            description="""
            Please provide the link(s) to the Tumblr blog where *the infringing (stolen) copy of the content* is located.

            *__Example:__ https://blog.tumblr.com/post/123456*
            """,
            color=embed_color
        )   

        await ctx.send(embed=step_3)   

        step_3_interaction = await bot.wait_for(
            "message", check=lambda msg: msg.author == ctx.author
        )

        # Final step: Go to the company's DMCA website

        final_step = discord.Embed(
            title="Continue to Tumblr's DMCA form to fill out your personal contact information.",
            description="""
            Click the button below to continue to Tumblr's DMCA form.
            """,
            color=embed_color        
        )
        
        online_form_btn = Button(style=ButtonStyle.green, label="🌐 Go to Tumblr DMCA form", custom_id="online_form_btn")

        await ctx.send(embed=final_step,components=[online_form_btn])

        final_step_interaction = await bot.wait_for(
            "button_click", check=lambda i: i.custom_id == "online_form_btn"
        )

        content_description = step_1_interaction.content
        original_links = step_2_interaction.content
        infringing_links = step_3_interaction.content

        browser = Browser('chrome')
        browser.visit("https://www.tumblr.com/dmca")
        description_box = browser.find_by_id("textarea_description").first
        description_box.fill(f"{content_description}") # Description of content
        original_links_box = browser.find_by_id("input_add_url").first
        original_links_box.fill(f"{original_links}")    # Links to your original content
        infringing_links_box = browser.find_by_id("infringing_url_popover").first
        infringing_links_box.fill(f"{infringing_links}") # Links to the infringing content

        complete = discord.Embed(
            title="What's next?",
            description="""
            Two things can happen next:
            1. Tumblr takes down the content you reported as stolen.
            2. If the alleged infringer does not think that their activity is infringing, they may file a DMCA counter-notice. Click [here](https://copyrightalliance.org/education/copyright-law-explained/the-digital-millennium-copyright-act-dmca/dmca-counter-notice-process/) to read more about counter-notices.
            """,
            color=embed_color        
        )   

        await ctx.send(embed=complete)     
    

bot.run(token)